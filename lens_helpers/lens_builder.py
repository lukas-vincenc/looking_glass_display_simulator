import bpy
from mathutils import Vector
from .lens_math import LensParameters, get_real_width
import math

LENS_CYLINDER_VERTICES = 512


def unite_objects(obj1, obj2):
    bool_mod = obj1.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'UNION'
    bool_mod.object = obj2

    bpy.context.view_layer.objects.active = obj1
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    bpy.data.objects.remove(obj2, do_unlink=True)


def flatten_lens_on_side(lens, side, lens_radius, lens_height, lens_depth, lens_width_percentage):
    flatten_offset = lens_radius * 0.5

    flatten_x = 1 - (lens_width_percentage / 100)

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(side * lens_radius * (1 - (flatten_x / 2)), flatten_offset, 0)
    )
    cube = bpy.context.object
    cube.name = "Flatten"

    cube.scale.x = lens_radius * flatten_x
    cube.scale.y = lens_radius * lens_depth * 2
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


def get_obj_dimensions(obj):
    bbox = [Vector(v) for v in obj.bound_box]

    size_x = max(v.x for v in bbox) - min(v.x for v in bbox)
    size_y = max(v.y for v in bbox) - min(v.y for v in bbox)
    size_z = max(v.z for v in bbox) - min(v.z for v in bbox)

    return size_x, size_y, size_z


def set_lens_location_rotation_and_scale(lens, params, display_width):
    if params.tilt < 0:
        rotation_compensation = display_width
        rotation_z = math.pi
    else:
        rotation_compensation = 0
        rotation_z = 0

    lens_width = get_real_width(params)

    lens.location.x = rotation_compensation + params.center * lens_width
    lens.location.y = -0.000001
    lens.location.z = 0

    lens.rotation_euler.y = abs(params.tilt)
    lens.rotation_euler.z = rotation_z


def resize_lens_to_correct_size(lens, params, base_dimensions):
    tilt_multiplier = -1 if params.tilt < 0 else 1

    base_x, base_y, base_z = base_dimensions
    lens_width = get_real_width(params)

    target_x = lens_width
    target_y = params.radius * params.depth * tilt_multiplier
    target_z = params.height

    sx = target_x / base_x
    sy = target_y / base_y
    sz = target_z / base_z

    for v in lens.data.vertices:
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz


def create_lens_cylinder(params):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=LENS_CYLINDER_VERTICES,
        radius=params.radius,
        depth=params.height,
        location=(0, 0, 0)
    )

    lens = bpy.context.object
    lens.name = "Lens"
    return lens


def create_lens_cube(params):
    depth_multiplier = params.depth - 1
    flatten_offset = params.radius * (depth_multiplier / 2)

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, flatten_offset, 0)
    )

    cube = bpy.context.object
    cube.name = "Flatten"

    cube.scale.x = params.radius * 2
    cube.scale.y = params.radius * depth_multiplier
    cube.scale.z = params.height

    return cube


def build_lens(params: LensParameters, material, display_width):
    lens = create_lens_cylinder(params)
    cube = create_lens_cube(params)

    unite_objects(lens, cube)

    flatten_lens_on_side(lens, -1, params.radius, params.height, params.depth, params.width_percentage)
    flatten_lens_on_side(lens, 1, params.radius, params.height, params.depth, params.width_percentage)

    if len(lens.data.materials) == 0:
        lens.data.materials.append(material)
    else:
        lens.data.materials[0] = material

    set_origin_bottom_center(lens)

    base_dimensions = get_obj_dimensions(lens)

    set_lens_location_rotation_and_scale(lens, params, display_width)

    lens["_base_size"] = base_dimensions
    lens["_base_mesh"] = lens.data.copy()

    resize_lens_to_correct_size(lens, params, base_dimensions)

    return lens
