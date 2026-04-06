import bpy
from mathutils import Vector
from .lens_math import LensParameters


def flatten_lens_on_side(lens, side, lens_radius, lens_height):
    # TODO: update to match technical report

    flatten_offset = lens_radius * 0.5

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(side * lens_radius, flatten_offset, 0)
    )
    cube = bpy.context.object
    cube.name = "Flatten"

    cube.scale.x = lens_radius / 1.5
    cube.scale.y = lens_radius * 3
    cube.scale.z = lens_height

    bool_mod = lens.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cube

    bpy.context.view_layer.objects.active = lens
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    bpy.data.objects.remove(cube, do_unlink=True)


def set_origin_bottom_center(obj):
    bbox = [Vector(v) for v in obj.bound_box]

    min_z = min(v.z for v in bbox)
    min_x = min(v.x for v in bbox)
    max_y = max(v.y for v in bbox)

    bottom_center_local = Vector((min_x, max_y, min_z))

    for v in obj.data.vertices:
        v.co -= bottom_center_local

    obj.location += obj.matrix_world.to_3x3() @ bottom_center_local


def build_lens(params: LensParameters, material):
    lens_radius = params.radius
    lens_height = params.height
    lens_tilt = params.tilt
    center = params.center
    cylinder_vertices = params.vertices

    flatten_offset = lens_radius * 0.8

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=cylinder_vertices,
        radius=lens_radius,
        depth=lens_height,
        location=(0, 0, 0)
    )

    lens = bpy.context.object
    lens.name = "Lens"

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, flatten_offset, 0)
    )

    cube = bpy.context.object
    cube.name = "Flatten"

    cube.scale.x = lens_radius * 2
    cube.scale.y = lens_radius * 1.6
    cube.scale.z = lens_height

    bool_mod = lens.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'UNION'
    bool_mod.object = cube

    bpy.context.view_layer.objects.active = lens
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    bpy.data.objects.remove(cube, do_unlink=True)

    flatten_lens_on_side(lens, -1, lens_radius, lens_height)
    flatten_lens_on_side(lens, 1, lens_radius, lens_height)

    lens.rotation_euler.y = abs(lens_tilt)

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
    lens.location.y = -0.000001
    lens.location.z = 0

    lens["_base_size"] = (size_x, size_y, size_z)
    lens["_base_mesh"] = lens.data.copy()

    return lens
