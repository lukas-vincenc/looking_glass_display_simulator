import math

import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty

from .display_spawner import DisplaySpawner


def recalc_lens_geometry(obj, custom_props, display_width):
    if "_base_mesh" not in obj or "_base_size" not in obj:
        return

    base_x, base_y, base_z = obj["_base_size"]

    lens_tilt = custom_props.lds_tilt
    center = custom_props.lds_center
    tilted_display_width = display_width * math.cos(lens_tilt)

    lens_radius = (tilted_display_width / custom_props.lds_pitch / 2) * (4 / 3)
    lens_height = display_width * custom_props.lds_height / custom_props.lds_width

    # Reset mesh
    obj.data = obj["_base_mesh"].copy()

    obj.location.x = center * lens_radius * 2 * (3 / 4)

    # Target dimensions
    target_x = lens_radius * 2 * (3 / 4)
    target_y = lens_radius * 2 * (3 / 4) + lens_radius
    target_z = lens_height

    sx = target_x / base_x
    sy = target_y / base_y
    sz = target_z / base_z

    for v in obj.data.vertices:
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz


def update_lens_tilt(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    obj.rotation_euler.y = self.lds_tilt
    recalc_lens_geometry(obj, context.scene.lds_custom_props, DisplaySpawner.DISPLAY_WIDTH)


def update_lens_pitch(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    arr_mod = obj.modifiers.get("Lens_Array")
    arr_mod.count = self.lds_pitch
    recalc_lens_geometry(obj, context.scene.lds_custom_props, DisplaySpawner.DISPLAY_WIDTH)


def update_lens_center(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    recalc_lens_geometry(obj, context.scene.lds_custom_props, DisplaySpawner.DISPLAY_WIDTH)


def update_aspect_ratio(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None:
        return

    recalc_lens_geometry(obj, context.scene.lds_custom_props, DisplaySpawner.DISPLAY_WIDTH)


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
    plane.location.y = 0

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
        min=-math.pi / 2,
        max=math.pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        precision=5,
        update=update_lens_tilt
    )
    lds_center: FloatProperty(
        name="Center",
        default=0,
        min=-1,
        max=1,
        update=update_lens_center
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
    bl_idname = "LENTICULAR_DISPLAY_SIMULATOR_PT_lds"
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
        layout.prop(cus_pt, "lds_center")

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
