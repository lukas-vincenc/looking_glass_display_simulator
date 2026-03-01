import math

import bpy
from mathutils import Vector


def get_lens_material():
    mat_name = "LensMaterial"
    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # clearing default nodes
        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)

        glass = nodes.new(type='ShaderNodeBsdfGlass')
        glass.location = (0, 0)
        glass.inputs['Roughness'].default_value = 0.0  # perfectly smooth
        glass.inputs['IOR'].default_value = 1.49  # acrylic glass
        glass.inputs['Color'].default_value = (1, 1, 1, 1)  # white

        links.new(glass.outputs['BSDF'], output.inputs['Surface'])
        return mat


def flatten_lens_on_side(lens, side, lens_radius, lens_height):
    flatten_offset = lens_radius * 0.5

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(side * lens_radius, flatten_offset, 0)
    )
    cube = bpy.context.object
    cube.name = f"Flatten"

    cube.scale.x = lens_radius / 2
    cube.scale.y = lens_radius * 3
    cube.scale.z = lens_height

    bool_mod = lens.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cube

    bpy.context.view_layer.objects.active = lens
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    # remove cube
    bpy.data.objects.remove(cube, do_unlink=True)


def set_origin_bottom_center(obj):
    # Get local-space bounding box
    bbox = [Vector(v) for v in obj.bound_box]

    min_z = min(v.z for v in bbox)
    min_x = min(v.x for v in bbox)
    max_y = max(v.y for v in bbox)

    bottom_center_local = Vector((min_x, max_y, min_z))

    # Move mesh data so origin shifts to bottom-center
    for v in obj.data.vertices:
        v.co -= bottom_center_local

    # Move object back so world position stays unchanged
    obj.location += obj.matrix_world.to_3x3() @ bottom_center_local


def get_lens(lens_radius, lens_height, lens_tilt, center, cylinder_vertices, material):
    flatten_offset = lens_radius * 0.5

    # creates a cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=cylinder_vertices,
        radius=lens_radius,
        depth=lens_height,
        location=(0, 0, 0)
    )
    lens = bpy.context.object
    lens.name = f"Lens"

    # creates a matching cube to flatten the cylinder
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, flatten_offset + 0.3 * lens_radius, 0)
    )
    cube = bpy.context.object
    cube.name = f"Flatten"

    cube.scale.x = lens_radius * 2
    cube.scale.y = lens_radius + 0.6 * lens_radius
    cube.scale.z = lens_height

    bool_mod = lens.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'UNION'
    bool_mod.object = cube

    bpy.context.view_layer.objects.active = lens
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    # remove cube
    bpy.data.objects.remove(cube, do_unlink=True)

    flatten_lens_on_side(lens, -1, lens_radius, lens_height)
    flatten_lens_on_side(lens, 1, lens_radius, lens_height)

    lens.rotation_euler.y = lens_tilt

    # assign lens material
    if len(lens.data.materials) == 0:
        lens.data.materials.append(material)
    else:
        lens.data.materials[0] = material

    set_origin_bottom_center(lens)

    bbox = [Vector(v) for v in lens.bound_box]
    size_x = max(v.x for v in bbox) - min(v.x for v in bbox)
    size_y = max(v.y for v in bbox) - min(v.y for v in bbox)
    size_z = max(v.z for v in bbox) - min(v.z for v in bbox)

    lens.location.x = center * lens_radius * 2 * (3 / 4)
    lens.location.y = - 0.000001

    lens["_base_size"] = (size_x, size_y, size_z)
    lens["_base_mesh"] = lens.data.copy()

    return lens


class DisplaySpawner(bpy.types.Operator):
    bl_idname = "object.display_spawner"
    bl_label = "Display Spawner"
    bl_description = "Spawns lenses creating the display"

    DISPLAY_WIDTH = 1

    def execute(self, context):
        scene = context.scene

        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'

        custom_props = scene.lds_custom_props

        lens_tilt = custom_props.lds_tilt
        center = custom_props.lds_center

        tilted_display_width = self.DISPLAY_WIDTH * math.cos(lens_tilt)

        lens_radius = (tilted_display_width / custom_props.lds_pitch / 2) * (4 / 3)
        lens_height = self.DISPLAY_WIDTH * custom_props.lds_height / custom_props.lds_width
        cylinder_vertices = 512

        # clear old lenses
        for obj in bpy.data.objects:
            if obj.name.startswith("Lens") or obj.name.startswith("Flatten_"):
                bpy.data.objects.remove(obj, do_unlink=True)

        material = get_lens_material()
        lens = get_lens(lens_radius, lens_height, lens_tilt, center, cylinder_vertices, material)

        array_mod = lens.modifiers.new(name="Lens_Array", type='ARRAY')
        array_mod.fit_type = 'FIXED_COUNT'
        array_mod.count = custom_props.lds_pitch

        return {'FINISHED'}
