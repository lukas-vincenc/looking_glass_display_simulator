import bpy
import math

from .quilt_interlacer_nodes import get_shader_node_tree


# Creates a material with an image texture appended to it
def get_material(img):
    mat = bpy.data.materials.new(name="ImageMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    tex_node = nodes.new(type="ShaderNodeTexImage")
    tex_node.image = img
    tex_node.location = (-400, 0)

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 100)

    emission = nodes.new(type="ShaderNodeEmission")
    emission.location = (0, -100)
    emission.inputs["Strength"].default_value = 1.0

    links.new(tex_node.outputs["Color"], emission.inputs["Color"])

    out = nodes.new(type="ShaderNodeOutputMaterial")
    out.location = (300, 0)

    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

    add_shader = nodes.new(type="ShaderNodeAddShader")
    add_shader.location = (150, 0)
    links.new(bsdf.outputs["BSDF"], add_shader.inputs[0])
    links.new(emission.outputs["Emission"], add_shader.inputs[1])
    links.new(add_shader.outputs["Shader"], out.inputs["Surface"])

    return mat


# Uses the input image and spawns it in the form of a plane with the image as its texture
def spawn_image_plane(img, context):
    bpy.ops.mesh.primitive_plane_add(size=1)
    plane = context.active_object
    plane.name = "ImagePlane"

    # Set correct aspect ratio
    plane.scale.y = 1.0 if img.size[0] == 0 else img.size[1] / img.size[0]
    plane.location.x = 0.5
    plane.location.y = 0
    plane.location.z = plane.scale.y / 2

    mat = get_material(img)

    plane.data.materials.append(mat)

    plane.rotation_euler = (math.pi / 2, 0, 0)


# Creates a plane, appends a shader node to it, which transforms the input quilt into the interlaced image
# As a result, user sees the interlaced image in the scene
def transform_quilt_and_spawn(img, context, pitch, tilt, center, subpixel, width, height, x_tiles, y_tiles):
    calibration = {
        'pitch': pitch,
        'tilt': math.tan(tilt) * (height / width),
        'center': center,
        'subpixel': subpixel,
        'x_tiles': x_tiles,
        'y_tiles': y_tiles
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

    mat = get_shader_node_tree(img, calibration)
    plane.data.materials.append(mat)

    return plane


# Called when user updates the interlaced image parameters
# Propagates the input values into the Shader Nodes setup
def update_display_image_params(calibration, width, height):
    mat = bpy.data.materials.get("Display_Image_Interlacer")
    if not mat or not mat.node_tree:
        return

    nodes = mat.node_tree.nodes

    if "Tilt" in nodes:
        nodes["Tilt"].outputs[0].default_value = math.tan(calibration['tilt']) * (height / width)
    if "Pitch" in nodes:
        nodes["Pitch"].outputs[0].default_value = calibration['pitch']
    if "Center" in nodes:
        nodes["Center"].outputs[0].default_value = calibration['center']
    if "Subpixel" in nodes:
        nodes["Subpixel"].outputs[0].default_value = calibration['subpixel']
    if "X_Tiles" in nodes:
        nodes["X_Tiles"].outputs[0].default_value = calibration['x_tiles']
    if "Y_Tiles" in nodes:
        nodes["Y_Tiles"].outputs[0].default_value = calibration['y_tiles']
