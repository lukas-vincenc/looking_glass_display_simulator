import math

import bmesh
import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty
from mathutils import Vector, Euler

from .display_spawner import DisplaySpawner


def lean_mesh_from_base_fixed(obj, rot_euler):
    """Lean mesh forward around base pivot without moving base in world space."""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # compute bottom-center pivot in object local space
    bbox = [Vector(v) for v in obj.bound_box]
    min_z = min(v.z for v in bbox)
    avg_x = sum(v.x for v in bbox) / 8
    avg_y = sum(v.y for v in bbox) / 8
    pivot = Vector((avg_x, avg_y, min_z))

    # compute horizontal offset introduced by rotation
    angle_y = rot_euler.y  # rotation around Y
    width = max(v.co.x for v in bm.verts) - min(v.co.x for v in bm.verts)

    horizontal_shift = pivot.x - (pivot.x * math.cos(angle_y) - width/2 * math.sin(angle_y))

    # apply rotation around pivot
    rot_mat = rot_euler.to_matrix().to_4x4()
    for v in bm.verts:
        v.co = rot_mat @ (v.co - pivot) + pivot

    # move mesh back so base stays fixed
    for v in bm.verts:
        v.co.x -= horizontal_shift

    bm.to_mesh(mesh)
    bm.free()


def restore_base_mesh(obj):
    base = obj.get("_base_mesh")
    if base is None:
        return

    bm = bmesh.new()
    bm.from_mesh(base)

    obj.data.clear_geometry()
    bm.to_mesh(obj.data)
    bm.free()


def update_lens_tilt(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    # restore original mesh (pre-lean)
    restore_base_mesh(obj)

    # apply lean
    lean_mesh_from_base_fixed(obj, Euler((0, self.lds_tilt, 0), 'XYZ'))


def update_lens_pitch(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    arr_mod = obj.modifiers.get("Lens_Array")
    arr_mod.count = self.lds_pitch


def update_aspect_ratio(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    obj.dimensions.z = self.lds_height / self.lds_width


def update_image_plane(self, context):
    path = self.lds_image_path
    if not path:
        return

    # Load image
    try:
        img = bpy.data.images.load(path, check_existing=True)
    except:
        print("Invalid image path")
        return

    # Remove old plane if exists
    if "ImagePlane" in bpy.data.objects:
        old = bpy.data.objects["ImagePlane"]
        bpy.data.objects.remove(old, do_unlink=True)

    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=1)
    plane = context.active_object
    plane.name = "ImagePlane"

    # Set correct aspect ratio
    plane.scale.y = 1.0 if img.size[0] == 0 else img.size[1] / img.size[0]
    plane.location.x = 0.5
    plane.location.y = 0.005

    # Create material
    mat = bpy.data.materials.new(name="ImageMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Image texture node
    tex_node = nodes.new(type="ShaderNodeTexImage")
    tex_node.image = img
    tex_node.location = (-400, 0)

    # Principled BSDF
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 100)

    # Emission node
    emission = nodes.new(type="ShaderNodeEmission")
    emission.location = (0, -100)
    emission.inputs["Strength"].default_value = 1.0
    # Connect image texture to emission color
    links.new(tex_node.outputs["Color"], emission.inputs["Color"])

    # Material Output
    out = nodes.new(type="ShaderNodeOutputMaterial")
    out.location = (300, 0)

    # Connect nodes
    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    # Mix emission and BSDF into surface output using Add Shader
    add_shader = nodes.new(type="ShaderNodeAddShader")
    add_shader.location = (150, 0)
    links.new(bsdf.outputs["BSDF"], add_shader.inputs[0])
    links.new(emission.outputs["Emission"], add_shader.inputs[1])
    links.new(add_shader.outputs["Shader"], out.inputs["Surface"])

    # Assign material
    plane.data.materials.append(mat)

    # Rotate plane to face upward
    plane.rotation_euler = (math.pi / 2, 0, 0)


# Custom properties shown in the extension UI panel
class CustomProps(bpy.types.PropertyGroup):
    lds_pitch: IntProperty(
        name="Pitch",
        default=355,
        min=1,
        max=1000,
        update=update_lens_pitch
    )
    lds_tilt: FloatProperty(
        name="Tilt",
        default=0,
        min=-math.pi/2,
        max=math.pi/2,
        subtype='ANGLE',
        unit='ROTATION',
        precision=5,
        update=update_lens_tilt
    )
    lds_image_path: StringProperty(
        name="Image",
        description="Select image to spawn as plane",
        subtype='FILE_PATH',
        update=update_image_plane
    )
    lds_width: FloatProperty(
        name="Width",
        default=16,
        min=1,
        max=1000,
        precision=2,
        update=update_aspect_ratio
    )
    lds_height: FloatProperty(
        name="Height",
        default=9,
        min=1,
        max=1000,
        precision=2,
        update=update_aspect_ratio
    )


class DisplaySimulatorPanel(bpy.types.Panel):
    bl_label = "Lenticular Display Simulator"
    bl_idname = "LENTICULAR DISPLAY SIMULATOR_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LentDisplay'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.lds_custom_props

        layout.label(text="Select display image:")
        layout.prop(cus_pt, "lds_image_path")

        layout.separator()

        layout.label(text="Display Aspect Ratio")

        layout.prop(cus_pt, "lds_width")
        layout.prop(cus_pt, "lds_height")

        layout.separator()

        layout.label(text="Display lens configuration")

        layout.prop(cus_pt, "lds_pitch")
        layout.prop(cus_pt, "lds_tilt")

        layout.operator("object.display_spawner", text="Spawn Display")


all_classes = [
    CustomProps,
    DisplaySimulatorPanel,
    DisplaySpawner
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lds_custom_props = bpy.props.PointerProperty(type=CustomProps)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lds_custom_props
