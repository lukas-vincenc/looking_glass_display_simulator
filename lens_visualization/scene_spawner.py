import math

import bpy

from . import refraction_geometry_nodes


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


def spawn_lens():
    target_coll = get_or_create_collection("Raycast_Targets")

    lens_radius = 1
    flatten_offset = lens_radius * 0.5
    cylinder_vertices = 512
    lens_height = 10

    # clear old lenses
    for obj in bpy.data.objects:
        if obj.name.startswith("Lens") or obj.name.startswith("Flatten"):
            bpy.data.objects.remove(obj, do_unlink=True)

    material = get_lens_material()

    # creates a cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=cylinder_vertices,
        radius=lens_radius,
        depth=lens_height,
        location=(0, 10, 0)
    )
    cyl = bpy.context.object
    cyl.name = f"Lens"

    move_object_to_collection(cyl, target_coll)

    # creates a matching cube to flatten the cylinder
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 10 + flatten_offset, 0)
    )
    cube = bpy.context.object
    cube.name = f"Flatten_Temp"

    cube.scale.x = lens_radius * 2.0
    cube.scale.y = lens_radius
    cube.scale.z = lens_height

    bool_mod = cyl.modifiers.new(name="FlatSide", type='BOOLEAN')
    bool_mod.operation = 'UNION'
    bool_mod.object = cube

    bpy.context.view_layer.objects.active = cyl
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    # remove cube
    bpy.data.objects.remove(cube, do_unlink=True)

    # assign lens material
    if len(cyl.data.materials) == 0:
        cyl.data.materials.append(material)
    else:
        cyl.data.materials[0] = material


def spawn_wall():
    target_coll = get_or_create_collection("Raycast_Targets")

    # clear old walls
    for obj in bpy.data.objects:
        if obj.name.startswith("Wall"):
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(
        size=100,
        location=(0, 20, 0),
        rotation=(math.pi * 0.5, 0, 0)
    )
    plane = bpy.context.object
    plane.name = f"Wall"

    move_object_to_collection(plane, target_coll)


def spawn_floor():
    # clear old floors
    for obj in bpy.data.objects:
        if obj.name.startswith("Floor"):
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(
        size=100,
        location=(0, 0, -10),
    )
    plane = bpy.context.object
    plane.name = f"Floor"


def spawn_ray_source():
    target_coll = get_or_create_collection("Ray_Source")
    # clear old sources
    for obj in bpy.data.objects:
        if obj.name.startswith("Ray"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # source used to control the ray
    bpy.ops.object.empty_add(
        type="SPHERE",
        location=(0, 0, 0),
        rotation=(0, 0, math.pi * 0.5),
    )
    ray_source = bpy.context.object
    ray_source.name = f"Ray_Source"

    move_object_to_collection(ray_source, target_coll)

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    ray = bpy.context.object
    ray.name = f"Ray"

    move_object_to_collection(ray, target_coll)

    nodes = ray.modifiers.new(name="GeometryNodes", type='NODES')
    nodes.node_group = refraction_geometry_nodes.get_node_tree()

    for item in refraction_geometry_nodes.get_node_tree().interface.items_tree:
        print(item.identifier, item.name, item.socket_type)

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


class SceneSpawner(bpy.types.Operator):
    bl_idname = "object.scene_spawner"
    bl_label = "Scene Spawner"
    bl_description = "Spawns a lens and a laser to simulate how light travels through it"

    def execute(self, context):
        spawn_lens()
        spawn_wall()
        # spawn_floor()
        spawn_ray_source()

        return {'FINISHED'}
