import math
import bpy

from ..lens_helpers.materials import get_lens_material
from ..lens_helpers.lens_builder import build_lens
from ..lens_helpers.lens_math import LensParameters

from . import refraction_geometry_nodes


def spawn_lens(depth, width_percentage):
    target_coll = get_or_create_collection("Raycast_Targets")

    lens_radius = 1
    lens_height = 10
    center = 0
    tilt = 0

    material = get_lens_material()

    params = LensParameters(
        radius=lens_radius,
        height=lens_height,
        depth=depth,
        width_percentage=width_percentage,
        tilt=tilt,
        center=center,
        missing_lenses=0,
    )

    lens = build_lens(params, material, 1)

    # match original location
    lens.location = (-(width_percentage / 100), 10, -5)

    move_object_to_collection(lens, target_coll)


def spawn_wall():
    target_coll = get_or_create_collection("Raycast_Targets")

    bpy.ops.mesh.primitive_plane_add(
        size=100,
        location=(0, 20, 0),
        rotation=(math.pi * 0.5, 0, 0)
    )

    plane = bpy.context.object
    plane.name = "Wall"

    move_object_to_collection(plane, target_coll)


def spawn_ray_source():
    target_coll = get_or_create_collection("Ray_Source")

    # source used to control the ray
    bpy.ops.object.empty_add(
        type="SPHERE",
        location=(0, 0, 0),
        rotation=(0, 0, math.pi * 0.5),
    )
    ray_source = bpy.context.object
    ray_source.name = "Ray_Source"

    move_object_to_collection(ray_source, target_coll)

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    ray = bpy.context.object
    ray.name = "Ray"

    move_object_to_collection(ray, target_coll)

    nodes = ray.modifiers.new(name="GeometryNodes", type='NODES')
    nodes.node_group = refraction_geometry_nodes.get_node_tree()

    nodes["Socket_2"] = ray_source
    nodes["Socket_3"] = get_or_create_collection("Raycast_Targets")
    nodes["Socket_4"] = 4.0


def get_or_create_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def move_object_to_collection(obj, target_coll):
    # link to collection
    if obj.name not in target_coll.objects:
        target_coll.objects.link(obj)

    # unlink from other top-level collections
    for coll in obj.users_collection:
        if coll != target_coll:
            coll.objects.unlink(obj)


def clear_scene():
    prefixes = ("Ray", "Wall", "Lens", "Flatten")

    for obj in bpy.data.objects:
        if obj.name.startswith(prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)


class SceneSpawner(bpy.types.Operator):
    bl_idname = "object.scene_spawner"
    bl_label = "Scene Spawner"
    bl_description = "Spawns a lens and a laser to simulate how light travels through it"

    def execute(self, context):
        scene = context.scene
        props = scene.lvis_custom_props

        clear_scene()
        spawn_lens(props.lens_depth, props.lens_width)
        spawn_wall()
        spawn_ray_source()

        return {'FINISHED'}
