import bpy

def get_node_tree(img, calibration):
    mat_name = "Display_Image_Interlacer"
    lkg_mat = bpy.data.materials.get(mat_name)

    if lkg_mat is None:
        lkg_mat = bpy.data.materials.new(name=mat_name)
        lkg_mat.use_nodes = True
        lkg_mat.blend_method = 'HASHED'

    shader_nodetree = lkg_mat.node_tree
    shader_nodetree.nodes.clear()

    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Separate XYZ
    separate_xyz = shader_nodetree.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Tilt"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = calibration['tilt']

    # Node Math.001
    math_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ADD'
    math_001.use_clamp = False

    # Node Math.002
    math_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_002.name = "Pitch"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = calibration['pitch']

    # Node Math.003
    math_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_003.name = "Center"
    math_003.operation = 'SUBTRACT'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = calibration['center']

    # Node Math.004
    math_004 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'FRACT'
    math_004.use_clamp = False

    total_tiles = calibration['tiles'][0] * calibration['tiles'][1]
    # Node Math.005
    math_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_005.name = "Total_Tiles"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = total_tiles

    # Node Math.006
    math_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'FLOOR'
    math_006.use_clamp = False

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.name = "X_Tiles.001"
    math_007.operation = 'MODULO'
    math_007.use_clamp = False
    # Value_001
    math_007.inputs[1].default_value = calibration['tiles'][0]

    # Node Math.008
    math_008 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_008.name = "X_Tiles.002"
    math_008.operation = 'DIVIDE'
    math_008.use_clamp = False
    # Value_001
    math_008.inputs[1].default_value = calibration['tiles'][0]

    # Node Math.009
    math_009 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'FLOOR'
    math_009.use_clamp = False

    # Node Combine XYZ
    combine_xyz = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Vector Math.001
    vector_math_001 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'

    # Node Vector Math.002
    vector_math_002 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Tiles_Vector"
    vector_math_002.operation = 'DIVIDE'
    # Vector_001
    vector_math_002.inputs[1].default_value = (calibration['tiles'][0], calibration['tiles'][1], 1.0)

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.image = img
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Linear'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Math.010
    math_010 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'SUBTRACT'
    math_010.use_clamp = False
    # Value
    math_010.inputs[0].default_value = 1.0

    # Set locations
    shader_nodetree.nodes["Texture Coordinate"].location = (-2015.266845703125, -759.2124633789062)
    shader_nodetree.nodes["Separate XYZ"].location = (-1762.279052734375, -470.37554931640625)
    shader_nodetree.nodes["Tilt"].location = (-1526.768798828125, -545.5394287109375)
    shader_nodetree.nodes["Math.001"].location = (-1358.44091796875, -437.4530029296875)
    shader_nodetree.nodes["Pitch"].location = (-1193.771728515625, -362.3416748046875)
    shader_nodetree.nodes["Center"].location = (-1003.48779296875, -312.87841796875)
    shader_nodetree.nodes["Math.004"].location = (-818.69287109375, -254.25535583496094)
    shader_nodetree.nodes["Total_Tiles"].location = (-650.36474609375, -193.80027770996094)
    shader_nodetree.nodes["Math.006"].location = (-469.2289733886719, -160.82481384277344)
    shader_nodetree.nodes["X_Tiles.001"].location = (-247.84092712402344, 4.052642822265625)
    shader_nodetree.nodes["X_Tiles.002"].location = (-202.09957885742188, -309.21453857421875)
    shader_nodetree.nodes["Math.009"].location = (-22.793540954589844, -234.10365295410156)
    shader_nodetree.nodes["Combine XYZ"].location = (125.40836334228516, -91.20978546142578)
    shader_nodetree.nodes["Vector Math.001"].location = (335.28546142578125, -387.7088928222656)
    shader_nodetree.nodes["Tiles_Vector"].location = (503.8307800292969, -77.16426086425781)
    shader_nodetree.nodes["Image Texture"].location = (679.1663818359375, 143.8504180908203)
    shader_nodetree.nodes["Emission"].location = (939.0389404296875, 168.9300994873047)
    shader_nodetree.nodes["Material Output"].location = (1101.8504638671875, 192.4423065185547)
    shader_nodetree.nodes["Math.010"].location = (-1546.6025390625, -327.1437683105469)

    # Set dimensions
    shader_nodetree.nodes["Texture Coordinate"].width = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Separate XYZ"].width = 140.0
    shader_nodetree.nodes["Separate XYZ"].height = 100.0

    shader_nodetree.nodes["Tilt"].width = 140.0
    shader_nodetree.nodes["Tilt"].height = 100.0

    shader_nodetree.nodes["Math.001"].width = 140.0
    shader_nodetree.nodes["Math.001"].height = 100.0

    shader_nodetree.nodes["Pitch"].width = 140.0
    shader_nodetree.nodes["Pitch"].height = 100.0

    shader_nodetree.nodes["Center"].width = 140.0
    shader_nodetree.nodes["Center"].height = 100.0

    shader_nodetree.nodes["Math.004"].width = 140.0
    shader_nodetree.nodes["Math.004"].height = 100.0

    shader_nodetree.nodes["Total_Tiles"].width = 140.0
    shader_nodetree.nodes["Total_Tiles"].height = 100.0

    shader_nodetree.nodes["Math.006"].width = 140.0
    shader_nodetree.nodes["Math.006"].height = 100.0

    shader_nodetree.nodes["X_Tiles.001"].width = 140.0
    shader_nodetree.nodes["X_Tiles.001"].height = 100.0

    shader_nodetree.nodes["X_Tiles.002"].width = 140.0
    shader_nodetree.nodes["X_Tiles.002"].height = 100.0

    shader_nodetree.nodes["Math.009"].width = 140.0
    shader_nodetree.nodes["Math.009"].height = 100.0

    shader_nodetree.nodes["Combine XYZ"].width = 140.0
    shader_nodetree.nodes["Combine XYZ"].height = 100.0

    shader_nodetree.nodes["Vector Math.001"].width = 140.0
    shader_nodetree.nodes["Vector Math.001"].height = 100.0

    shader_nodetree.nodes["Tiles_Vector"].width = 140.0
    shader_nodetree.nodes["Tiles_Vector"].height = 100.0

    shader_nodetree.nodes["Image Texture"].width = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Emission"].width = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Material Output"].width = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Math.010"].width = 140.0
    shader_nodetree.nodes["Math.010"].height = 100.0

    # Initialize shader_nodetree links

    # texture_coordinate.UV -> separate_xyz.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[2],
        shader_nodetree.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.Y -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ"].outputs[1],
        shader_nodetree.nodes["Tilt"].inputs[0]
    )
    # math.Value -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tilt"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[1]
    )
    # math_001.Value -> math_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Pitch"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch"].outputs[0],
        shader_nodetree.nodes["Center"].inputs[0]
    )
    # math_003.Value -> math_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center"].outputs[0],
        shader_nodetree.nodes["Math.004"].inputs[0]
    )
    # math_004.Value -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.004"].outputs[0],
        shader_nodetree.nodes["Total_Tiles"].inputs[0]
    )
    # math_005.Value -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Total_Tiles"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[0]
    )
    # math_006.Value -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["X_Tiles.001"].inputs[0]
    )
    # math_006.Value -> math_008.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["X_Tiles.002"].inputs[0]
    )
    # math_008.Value -> math_009.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.002"].outputs[0],
        shader_nodetree.nodes["Math.009"].inputs[0]
    )
    # math_007.Value -> combine_xyz.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.001"].outputs[0],
        shader_nodetree.nodes["Combine XYZ"].inputs[0]
    )
    # math_009.Value -> combine_xyz.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.009"].outputs[0],
        shader_nodetree.nodes["Combine XYZ"].inputs[1]
    )
    # combine_xyz.Vector -> vector_math_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ"].outputs[0],
        shader_nodetree.nodes["Vector Math.001"].inputs[0]
    )
    # texture_coordinate.UV -> vector_math_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[2],
        shader_nodetree.nodes["Vector Math.001"].inputs[1]
    )
    # vector_math_001.Vector -> vector_math_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.001"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector"].inputs[0]
    )
    # vector_math_002.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tiles_Vector"].outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # image_texture.Color -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # emission.Emission -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # separate_xyz.X -> math_010.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ"].outputs[0],
        shader_nodetree.nodes["Math.010"].inputs[1]
    )
    # math_010.Value -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.010"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[0]
    )

    return lkg_mat
