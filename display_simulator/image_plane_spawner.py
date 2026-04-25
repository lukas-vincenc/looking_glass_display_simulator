import bpy
import math

from ..lens_helpers.lens_builder import set_origin_bottom_center
from ..quilt_maker.display_image_interlacer_nodes import get_node_tree


def get_material(img):
    mat = bpy.data.materials.new(name="ImageMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

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

    # Mix emission and BSDF into surface output
    add_shader = nodes.new(type="ShaderNodeAddShader")
    add_shader.location = (150, 0)
    links.new(bsdf.outputs["BSDF"], add_shader.inputs[0])
    links.new(emission.outputs["Emission"], add_shader.inputs[1])
    links.new(add_shader.outputs["Shader"], out.inputs["Surface"])

    return mat


def spawn_image_plane(img, context):
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=1)
    plane = context.active_object
    plane.name = "ImagePlane"

    # Set correct aspect ratio
    plane.scale.y = 1.0 if img.size[0] == 0 else img.size[1] / img.size[0]
    plane.location.x = 0.5
    plane.location.y = 0
    plane.location.z = plane.scale.y / 2

    mat = get_material(img)

    # Assign material
    plane.data.materials.append(mat)

    # Rotate plane to face upward
    plane.rotation_euler = (math.pi / 2, 0, 0)


def transform_quilt_and_spawn(img, context, pitch, tilt, center, width, height, x_tiles, y_tiles):
    calibration = {
        'pitch': pitch,
        'tilt': tilt * (height / width),
        'center': center,
        'tiles': (x_tiles, y_tiles)
    }

    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(0.5, 0, height / (width * 2)),
    )
    plane = context.active_object
    plane.name = "ImagePlane"

    plane.scale.x = 1.0
    plane.scale.y = height / width
    plane.rotation_euler = (math.pi / 2, 0, 0)

    mat = get_node_tree(img, calibration)
    plane.data.materials.append(mat)

    return plane


def update_display_image_params(pitch, tilt, center, width, height, x_tiles, y_tiles):
    mat = bpy.data.materials.get("Display_Image_Interlacer")
    if not mat or not mat.node_tree:
        return

    nodes = mat.node_tree.nodes

    if "Tilt" in nodes:
        nodes["Tilt"].inputs[1].default_value = tilt * (height / width)
    if "Pitch" in nodes:
        nodes["Pitch"].inputs[1].default_value = pitch
    if "Center" in nodes:
        nodes["Center"].inputs[1].default_value = center
    if "Total_Tiles" in nodes:
        nodes["Total_Tiles"].inputs[1].default_value = x_tiles * y_tiles
    if "X_Tiles.001" in nodes:
        nodes["X_Tiles.001"].inputs[1].default_value = x_tiles
    if "X_Tiles.002" in nodes:
        nodes["X_Tiles.002"].inputs[1].default_value = x_tiles
    if "Tiles_Vector" in nodes:
        nodes["Tiles_Vector"].inputs[1].default_value = (x_tiles, y_tiles, 1.0)
