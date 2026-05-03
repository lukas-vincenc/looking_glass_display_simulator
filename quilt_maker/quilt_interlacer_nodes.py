import bpy


def get_node_tree(img, calibration):
    mat_name = "Display_Image_Interlacer"
    lkg_mat = bpy.data.materials.get(mat_name)

    if lkg_mat is None:
        lkg_mat = bpy.data.materials.new(name=mat_name)
        lkg_mat.use_nodes = True
        lkg_mat.blend_method = 'HASHED'

    shader_nodetree = lkg_mat.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.hide = True
    texture_coordinate.from_instancer = False

    # Node Pitch.000
    pitch_000 = shader_nodetree.nodes.new("ShaderNodeMath")
    pitch_000.name = "Pitch.000"
    pitch_000.hide = True
    pitch_000.operation = 'MULTIPLY'
    pitch_000.use_clamp = False

    # Node Center.000
    center_000 = shader_nodetree.nodes.new("ShaderNodeMath")
    center_000.name = "Center.000"
    center_000.hide = True
    center_000.operation = 'SUBTRACT'
    center_000.use_clamp = False

    # Node Total_Tiles
    total_tiles = shader_nodetree.nodes.new("ShaderNodeMath")
    total_tiles.name = "Total_Tiles"
    total_tiles.hide = True
    total_tiles.operation = 'MULTIPLY'
    total_tiles.use_clamp = False

    # Node Math.006
    math_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.hide = True
    math_006.operation = 'FLOOR'
    math_006.use_clamp = False

    # Node X_Tiles.001
    x_tiles_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_001.name = "X_Tiles.001"
    x_tiles_001.hide = True
    x_tiles_001.operation = 'MODULO'
    x_tiles_001.use_clamp = False

    # Node X_Tiles.002
    x_tiles_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_002.name = "X_Tiles.002"
    x_tiles_002.hide = True
    x_tiles_002.operation = 'DIVIDE'
    x_tiles_002.use_clamp = False

    # Node Math.009
    math_009 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.hide = True
    math_009.operation = 'FLOOR'
    math_009.use_clamp = False

    # Node Combine XYZ
    combine_xyz = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    combine_xyz.hide = True
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Vector Math.001
    vector_math_001 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.hide = True
    vector_math_001.operation = 'ADD'

    # Node Tiles_Vector
    tiles_vector = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    tiles_vector.name = "Tiles_Vector"
    tiles_vector.hide = True
    tiles_vector.operation = 'DIVIDE'

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

    # Node Pitch.001
    pitch_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    pitch_001.name = "Pitch.001"
    pitch_001.hide = True
    pitch_001.operation = 'MULTIPLY'
    pitch_001.use_clamp = False

    # Node Center.001
    center_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    center_001.name = "Center.001"
    center_001.hide = True
    center_001.operation = 'SUBTRACT'
    center_001.use_clamp = False

    # Node Total_Tiles.001
    total_tiles_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    total_tiles_001.name = "Total_Tiles.001"
    total_tiles_001.hide = True
    total_tiles_001.operation = 'MULTIPLY'
    total_tiles_001.use_clamp = False

    # Node Math.007
    math_007 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.hide = True
    math_007.operation = 'FLOOR'
    math_007.use_clamp = False

    # Node X_Tiles.003
    x_tiles_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_003.name = "X_Tiles.003"
    x_tiles_003.hide = True
    x_tiles_003.operation = 'MODULO'
    x_tiles_003.use_clamp = False

    # Node X_Tiles.004
    x_tiles_004 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_004.name = "X_Tiles.004"
    x_tiles_004.hide = True
    x_tiles_004.operation = 'DIVIDE'
    x_tiles_004.use_clamp = False

    # Node Math.011
    math_011 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.hide = True
    math_011.operation = 'FLOOR'
    math_011.use_clamp = False

    # Node Combine XYZ.001
    combine_xyz_001 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    combine_xyz_001.hide = True
    # Z
    combine_xyz_001.inputs[2].default_value = 0.0

    # Node Vector Math.002
    vector_math_002 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.hide = True
    vector_math_002.operation = 'ADD'

    # Node Tiles_Vector.001
    tiles_vector_001 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    tiles_vector_001.name = "Tiles_Vector.001"
    tiles_vector_001.hide = True
    tiles_vector_001.operation = 'DIVIDE'

    # Node Image Texture.001
    image_texture_001 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_001.name = "Image Texture.001"
    image_texture_001.extension = 'REPEAT'
    image_texture_001.image = img
    image_texture_001.image_user.frame_current = 0
    image_texture_001.image_user.frame_duration = 100
    image_texture_001.image_user.frame_offset = 0
    image_texture_001.image_user.frame_start = 1
    image_texture_001.image_user.tile = 0
    image_texture_001.image_user.use_auto_refresh = False
    image_texture_001.image_user.use_cyclic = False
    image_texture_001.interpolation = 'Linear'
    image_texture_001.projection = 'FLAT'
    image_texture_001.projection_blend = 0.0

    # Node Math
    math = shader_nodetree.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.hide = True
    math.operation = 'ADD'
    math.use_clamp = False

    # Node Separate Color
    separate_color = shader_nodetree.nodes.new("ShaderNodeSeparateColor")
    separate_color.name = "Separate Color"
    separate_color.mode = 'RGB'

    # Node Combine Color
    combine_color = shader_nodetree.nodes.new("ShaderNodeCombineColor")
    combine_color.name = "Combine Color"
    combine_color.mode = 'RGB'

    # Node Separate Color.001
    separate_color_001 = shader_nodetree.nodes.new("ShaderNodeSeparateColor")
    separate_color_001.name = "Separate Color.001"
    separate_color_001.mode = 'RGB'

    # Node Subpixel
    subpixel = shader_nodetree.nodes.new("ShaderNodeValue")
    subpixel.name = "Subpixel"

    subpixel.outputs[0].default_value = calibration['subpixel']
    # Node Pitch.002
    pitch_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    pitch_002.name = "Pitch.002"
    pitch_002.hide = True
    pitch_002.operation = 'MULTIPLY'
    pitch_002.use_clamp = False

    # Node Center.002
    center_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    center_002.name = "Center.002"
    center_002.hide = True
    center_002.operation = 'SUBTRACT'
    center_002.use_clamp = False

    # Node Total_Tiles.002
    total_tiles_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    total_tiles_002.name = "Total_Tiles.002"
    total_tiles_002.hide = True
    total_tiles_002.operation = 'MULTIPLY'
    total_tiles_002.use_clamp = False

    # Node Math.013
    math_013 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.hide = True
    math_013.operation = 'FLOOR'
    math_013.use_clamp = False

    # Node X_Tiles.005
    x_tiles_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_005.name = "X_Tiles.005"
    x_tiles_005.hide = True
    x_tiles_005.operation = 'MODULO'
    x_tiles_005.use_clamp = False

    # Node X_Tiles.006
    x_tiles_006 = shader_nodetree.nodes.new("ShaderNodeMath")
    x_tiles_006.name = "X_Tiles.006"
    x_tiles_006.hide = True
    x_tiles_006.operation = 'DIVIDE'
    x_tiles_006.use_clamp = False

    # Node Math.014
    math_014 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.hide = True
    math_014.operation = 'FLOOR'
    math_014.use_clamp = False

    # Node Combine XYZ.002
    combine_xyz_002 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_002.name = "Combine XYZ.002"
    combine_xyz_002.hide = True
    # Z
    combine_xyz_002.inputs[2].default_value = 0.0

    # Node Vector Math.003
    vector_math_003 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.hide = True
    vector_math_003.operation = 'ADD'

    # Node Tiles_Vector.002
    tiles_vector_002 = shader_nodetree.nodes.new("ShaderNodeVectorMath")
    tiles_vector_002.name = "Tiles_Vector.002"
    tiles_vector_002.hide = True
    tiles_vector_002.operation = 'DIVIDE'

    # Node Image Texture.002
    image_texture_002 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_002.name = "Image Texture.002"
    image_texture_002.extension = 'REPEAT'
    image_texture_002.image = img
    image_texture_002.image_user.frame_current = 0
    image_texture_002.image_user.frame_duration = 100
    image_texture_002.image_user.frame_offset = 0
    image_texture_002.image_user.frame_start = 1
    image_texture_002.image_user.tile = 0
    image_texture_002.image_user.use_auto_refresh = False
    image_texture_002.image_user.use_cyclic = False
    image_texture_002.interpolation = 'Linear'
    image_texture_002.projection = 'FLAT'
    image_texture_002.projection_blend = 0.0

    # Node Math.016
    math_016 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.hide = True
    math_016.operation = 'ADD'
    math_016.use_clamp = False

    # Node Texture Coordinate.001
    texture_coordinate_001 = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.name = "Texture Coordinate.001"
    texture_coordinate_001.hide = True
    texture_coordinate_001.from_instancer = False

    # Node Math.017
    math_017 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'MULTIPLY'
    math_017.use_clamp = False
    # Value_001
    math_017.inputs[1].default_value = 2.0

    # Node Separate Color.002
    separate_color_002 = shader_nodetree.nodes.new("ShaderNodeSeparateColor")
    separate_color_002.name = "Separate Color.002"
    separate_color_002.mode = 'RGB'

    # Node Pitch
    pitch = shader_nodetree.nodes.new("ShaderNodeValue")
    pitch.name = "Pitch"

    pitch.outputs[0].default_value = calibration['pitch']
    # Node Tilt
    tilt = shader_nodetree.nodes.new("ShaderNodeValue")
    tilt.name = "Tilt"

    tilt.outputs[0].default_value = calibration['tilt']
    # Node Center
    center = shader_nodetree.nodes.new("ShaderNodeValue")
    center.name = "Center"

    center.outputs[0].default_value = calibration['center']
    # Node Texture Coordinate.002
    texture_coordinate_002 = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_002.name = "Texture Coordinate.002"
    texture_coordinate_002.from_instancer = False

    # Node Separate XYZ.003
    separate_xyz_003 = shader_nodetree.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"

    # Node Tilt.003
    tilt_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    tilt_003.name = "Tilt.003"
    tilt_003.operation = 'MULTIPLY'
    tilt_003.use_clamp = False

    # Node Math.018
    math_018 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'ADD'
    math_018.use_clamp = False

    # Node Math.019
    math_019 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'SUBTRACT'
    math_019.use_clamp = False
    # Value
    math_019.inputs[0].default_value = 1.0

    # Node Texture Coordinate.003
    texture_coordinate_003 = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_003.name = "Texture Coordinate.003"
    texture_coordinate_003.hide = True
    texture_coordinate_003.from_instancer = False

    # Node Combine XYZ.003
    combine_xyz_003 = shader_nodetree.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.name = "Combine XYZ.003"
    combine_xyz_003.hide = True
    # Z
    combine_xyz_003.inputs[2].default_value = 1.0

    # Node X_Tiles
    x_tiles = shader_nodetree.nodes.new("ShaderNodeValue")
    x_tiles.name = "X_Tiles"

    x_tiles.outputs[0].default_value = calibration['x_tiles']
    # Node Y_Tiles
    y_tiles = shader_nodetree.nodes.new("ShaderNodeValue")
    y_tiles.name = "Y_Tiles"

    y_tiles.outputs[0].default_value = calibration['y_tiles']
    # Node Math.001
    math_001 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.hide = True
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False

    # Node Math.002
    math_002 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.hide = True
    math_002.operation = 'ABSOLUTE'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.hide = True
    math_003.operation = 'CEIL'
    math_003.use_clamp = False

    # Node Math.010
    math_010 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.hide = True
    math_010.operation = 'ADD'
    math_010.use_clamp = False

    # Node Math.004
    math_004 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.hide = True
    math_004.operation = 'ABSOLUTE'
    math_004.use_clamp = False

    # Node Math.012
    math_012 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.hide = True
    math_012.operation = 'CEIL'
    math_012.use_clamp = False

    # Node Math.015
    math_015 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.hide = True
    math_015.operation = 'ADD'
    math_015.use_clamp = False

    # Node Math.005
    math_005 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.hide = True
    math_005.operation = 'ABSOLUTE'
    math_005.use_clamp = False

    # Node Math.020
    math_020 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.hide = True
    math_020.operation = 'CEIL'
    math_020.use_clamp = False

    # Node Math.021
    math_021 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.hide = True
    math_021.operation = 'ADD'
    math_021.use_clamp = False

    # Node Math.022
    math_022 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.hide = True
    math_022.operation = 'FRACT'
    math_022.use_clamp = False

    # Node Math.023
    math_023 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.hide = True
    math_023.operation = 'FRACT'
    math_023.use_clamp = False

    # Node Math.008
    math_008 = shader_nodetree.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.hide = True
    math_008.operation = 'FRACT'
    math_008.use_clamp = False

    # Set locations
    shader_nodetree.nodes["Texture Coordinate"].location = (223.6524658203125, -290.7900695800781)
    shader_nodetree.nodes["Pitch.000"].location = (-1497.6029052734375, -277.7557373046875)
    shader_nodetree.nodes["Center.000"].location = (-1272.3961181640625, -291.26129150390625)
    shader_nodetree.nodes["Total_Tiles"].location = (-366.87860107421875, -222.2712860107422)
    shader_nodetree.nodes["Math.006"].location = (-206.6947784423828, -222.30101013183594)
    shader_nodetree.nodes["X_Tiles.001"].location = (60.6885871887207, -76.204345703125)
    shader_nodetree.nodes["X_Tiles.002"].location = (-46.657405853271484, -264.41668701171875)
    shader_nodetree.nodes["Math.009"].location = (126.2074966430664, -206.39559936523438)
    shader_nodetree.nodes["Combine XYZ"].location = (351.73974609375, -119.85843658447266)
    shader_nodetree.nodes["Vector Math.001"].location = (567.1362915039062, -191.91131591796875)
    shader_nodetree.nodes["Tiles_Vector"].location = (793.53271484375, -129.19403076171875)
    shader_nodetree.nodes["Image Texture"].location = (1077.5540771484375, 90.5197525024414)
    shader_nodetree.nodes["Emission"].location = (2181.682373046875, -535.5839233398438)
    shader_nodetree.nodes["Material Output"].location = (2344.7373046875, -533.2791748046875)
    shader_nodetree.nodes["Pitch.001"].location = (-1264.8001708984375, -1147.98095703125)
    shader_nodetree.nodes["Center.001"].location = (-1101.92529296875, -1220.4615478515625)
    shader_nodetree.nodes["Total_Tiles.001"].location = (-204.9828643798828, -1007.2855224609375)
    shader_nodetree.nodes["Math.007"].location = (-19.84230613708496, -1022.415283203125)
    shader_nodetree.nodes["X_Tiles.003"].location = (195.2322540283203, -882.2002563476562)
    shader_nodetree.nodes["X_Tiles.004"].location = (196.59654235839844, -1125.7672119140625)
    shader_nodetree.nodes["Math.011"].location = (415.91363525390625, -983.44873046875)
    shader_nodetree.nodes["Combine XYZ.001"].location = (588.1442260742188, -931.4202880859375)
    shader_nodetree.nodes["Vector Math.002"].location = (803.3943481445312, -996.5770263671875)
    shader_nodetree.nodes["Tiles_Vector.001"].location = (959.8919677734375, -830.5181884765625)
    shader_nodetree.nodes["Image Texture.001"].location = (1170.09228515625, -594.5465087890625)
    shader_nodetree.nodes["Math"].location = (-1513.322509765625, -1355.3642578125)
    shader_nodetree.nodes["Separate Color"].location = (1344.111083984375, 90.28633880615234)
    shader_nodetree.nodes["Combine Color"].location = (2020.257568359375, -515.13232421875)
    shader_nodetree.nodes["Separate Color.001"].location = (1435.170166015625, -548.27880859375)
    shader_nodetree.nodes["Subpixel"].location = (-2602.1435546875, -1767.5487060546875)
    shader_nodetree.nodes["Pitch.002"].location = (-1200.474853515625, -1957.10205078125)
    shader_nodetree.nodes["Center.002"].location = (-1033.2301025390625, -2062.158203125)
    shader_nodetree.nodes["Total_Tiles.002"].location = (-189.28109741210938, -1979.340087890625)
    shader_nodetree.nodes["Math.013"].location = (-37.589866638183594, -1912.4056396484375)
    shader_nodetree.nodes["X_Tiles.005"].location = (208.91351318359375, -1803.156005859375)
    shader_nodetree.nodes["X_Tiles.006"].location = (176.7263946533203, -2057.196044921875)
    shader_nodetree.nodes["Math.014"].location = (389.6745910644531, -1929.3865966796875)
    shader_nodetree.nodes["Combine XYZ.002"].location = (559.8037109375, -1842.20947265625)
    shader_nodetree.nodes["Vector Math.003"].location = (774.1719360351562, -1894.947998046875)
    shader_nodetree.nodes["Tiles_Vector.002"].location = (948.3463745117188, -1757.2518310546875)
    shader_nodetree.nodes["Image Texture.002"].location = (1194.5126953125, -1504.21435546875)
    shader_nodetree.nodes["Math.016"].location = (-1401.709716796875, -2089.0986328125)
    shader_nodetree.nodes["Texture Coordinate.001"].location = (396.7052917480469, -2025.22802734375)
    shader_nodetree.nodes["Math.017"].location = (-1623.5, -2088.139404296875)
    shader_nodetree.nodes["Separate Color.002"].location = (1461.216064453125, -1496.1629638671875)
    shader_nodetree.nodes["Pitch"].location = (-2593.12109375, -1276.0816650390625)
    shader_nodetree.nodes["Tilt"].location = (-2989.593994140625, -1129.771728515625)
    shader_nodetree.nodes["Center"].location = (-2590.493408203125, -1487.32421875)
    shader_nodetree.nodes["Texture Coordinate.002"].location = (-3250.188720703125, -1193.2347412109375)
    shader_nodetree.nodes["Separate XYZ.003"].location = (-2997.200927734375, -904.3978271484375)
    shader_nodetree.nodes["Tilt.003"].location = (-2761.690673828125, -979.5617065429688)
    shader_nodetree.nodes["Math.018"].location = (-2593.362548828125, -871.4752807617188)
    shader_nodetree.nodes["Math.019"].location = (-2781.524169921875, -761.1660766601562)
    shader_nodetree.nodes["Texture Coordinate.003"].location = (435.0686950683594, -1090.4034423828125)
    shader_nodetree.nodes["Combine XYZ.003"].location = (-1031.084716796875, -535.958740234375)
    shader_nodetree.nodes["X_Tiles"].location = (-1245.59375, -628.2725830078125)
    shader_nodetree.nodes["Y_Tiles"].location = (-1248.713623046875, -717.2796630859375)
    shader_nodetree.nodes["Math.001"].location = (-1015.7100830078125, -863.4052124023438)
    shader_nodetree.nodes["Math.002"].location = (-1120.292724609375, -335.02587890625)
    shader_nodetree.nodes["Math.003"].location = (-949.1890869140625, -336.1178894042969)
    shader_nodetree.nodes["Math.010"].location = (-726.731689453125, -209.10203552246094)
    shader_nodetree.nodes["Math.004"].location = (-916.7691650390625, -1216.226318359375)
    shader_nodetree.nodes["Math.012"].location = (-724.9312744140625, -1208.093994140625)
    shader_nodetree.nodes["Math.015"].location = (-565.3173217773438, -1128.93994140625)
    shader_nodetree.nodes["Math.005"].location = (-882.7664184570312, -2121.790283203125)
    shader_nodetree.nodes["Math.020"].location = (-711.662841796875, -2122.88232421875)
    shader_nodetree.nodes["Math.021"].location = (-544.22509765625, -2067.17138671875)
    shader_nodetree.nodes["Math.022"].location = (-385.0, -1084.0211181640625)
    shader_nodetree.nodes["Math.023"].location = (-369.7724609375, -2029.20703125)
    shader_nodetree.nodes["Math.008"].location = (-546.9998779296875, -220.1468505859375)

    # Set dimensions
    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Pitch.000"].width  = 140.0
    shader_nodetree.nodes["Pitch.000"].height = 100.0

    shader_nodetree.nodes["Center.000"].width  = 140.0
    shader_nodetree.nodes["Center.000"].height = 100.0

    shader_nodetree.nodes["Total_Tiles"].width  = 140.0
    shader_nodetree.nodes["Total_Tiles"].height = 100.0

    shader_nodetree.nodes["Math.006"].width  = 140.0
    shader_nodetree.nodes["Math.006"].height = 100.0

    shader_nodetree.nodes["X_Tiles.001"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.001"].height = 100.0

    shader_nodetree.nodes["X_Tiles.002"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.002"].height = 100.0

    shader_nodetree.nodes["Math.009"].width  = 140.0
    shader_nodetree.nodes["Math.009"].height = 100.0

    shader_nodetree.nodes["Combine XYZ"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ"].height = 100.0

    shader_nodetree.nodes["Vector Math.001"].width  = 140.0
    shader_nodetree.nodes["Vector Math.001"].height = 100.0

    shader_nodetree.nodes["Tiles_Vector"].width  = 140.0
    shader_nodetree.nodes["Tiles_Vector"].height = 100.0

    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Pitch.001"].width  = 140.0
    shader_nodetree.nodes["Pitch.001"].height = 100.0

    shader_nodetree.nodes["Center.001"].width  = 140.0
    shader_nodetree.nodes["Center.001"].height = 100.0

    shader_nodetree.nodes["Total_Tiles.001"].width  = 140.0
    shader_nodetree.nodes["Total_Tiles.001"].height = 100.0

    shader_nodetree.nodes["Math.007"].width  = 140.0
    shader_nodetree.nodes["Math.007"].height = 100.0

    shader_nodetree.nodes["X_Tiles.003"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.003"].height = 100.0

    shader_nodetree.nodes["X_Tiles.004"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.004"].height = 100.0

    shader_nodetree.nodes["Math.011"].width  = 140.0
    shader_nodetree.nodes["Math.011"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.001"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.001"].height = 100.0

    shader_nodetree.nodes["Vector Math.002"].width  = 140.0
    shader_nodetree.nodes["Vector Math.002"].height = 100.0

    shader_nodetree.nodes["Tiles_Vector.001"].width  = 140.0
    shader_nodetree.nodes["Tiles_Vector.001"].height = 100.0

    shader_nodetree.nodes["Image Texture.001"].width  = 240.0
    shader_nodetree.nodes["Image Texture.001"].height = 100.0

    shader_nodetree.nodes["Math"].width  = 140.0
    shader_nodetree.nodes["Math"].height = 100.0

    shader_nodetree.nodes["Separate Color"].width  = 140.0
    shader_nodetree.nodes["Separate Color"].height = 100.0

    shader_nodetree.nodes["Combine Color"].width  = 140.0
    shader_nodetree.nodes["Combine Color"].height = 100.0

    shader_nodetree.nodes["Separate Color.001"].width  = 140.0
    shader_nodetree.nodes["Separate Color.001"].height = 100.0

    shader_nodetree.nodes["Subpixel"].width  = 140.0
    shader_nodetree.nodes["Subpixel"].height = 100.0

    shader_nodetree.nodes["Pitch.002"].width  = 140.0
    shader_nodetree.nodes["Pitch.002"].height = 100.0

    shader_nodetree.nodes["Center.002"].width  = 140.0
    shader_nodetree.nodes["Center.002"].height = 100.0

    shader_nodetree.nodes["Total_Tiles.002"].width  = 140.0
    shader_nodetree.nodes["Total_Tiles.002"].height = 100.0

    shader_nodetree.nodes["Math.013"].width  = 140.0
    shader_nodetree.nodes["Math.013"].height = 100.0

    shader_nodetree.nodes["X_Tiles.005"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.005"].height = 100.0

    shader_nodetree.nodes["X_Tiles.006"].width  = 140.0
    shader_nodetree.nodes["X_Tiles.006"].height = 100.0

    shader_nodetree.nodes["Math.014"].width  = 140.0
    shader_nodetree.nodes["Math.014"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.002"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.002"].height = 100.0

    shader_nodetree.nodes["Vector Math.003"].width  = 140.0
    shader_nodetree.nodes["Vector Math.003"].height = 100.0

    shader_nodetree.nodes["Tiles_Vector.002"].width  = 140.0
    shader_nodetree.nodes["Tiles_Vector.002"].height = 100.0

    shader_nodetree.nodes["Image Texture.002"].width  = 240.0
    shader_nodetree.nodes["Image Texture.002"].height = 100.0

    shader_nodetree.nodes["Math.016"].width  = 140.0
    shader_nodetree.nodes["Math.016"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate.001"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate.001"].height = 100.0

    shader_nodetree.nodes["Math.017"].width  = 140.0
    shader_nodetree.nodes["Math.017"].height = 100.0

    shader_nodetree.nodes["Separate Color.002"].width  = 140.0
    shader_nodetree.nodes["Separate Color.002"].height = 100.0

    shader_nodetree.nodes["Pitch"].width  = 140.0
    shader_nodetree.nodes["Pitch"].height = 100.0

    shader_nodetree.nodes["Tilt"].width  = 140.0
    shader_nodetree.nodes["Tilt"].height = 100.0

    shader_nodetree.nodes["Center"].width  = 140.0
    shader_nodetree.nodes["Center"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate.002"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate.002"].height = 100.0

    shader_nodetree.nodes["Separate XYZ.003"].width  = 140.0
    shader_nodetree.nodes["Separate XYZ.003"].height = 100.0

    shader_nodetree.nodes["Tilt.003"].width  = 140.0
    shader_nodetree.nodes["Tilt.003"].height = 100.0

    shader_nodetree.nodes["Math.018"].width  = 140.0
    shader_nodetree.nodes["Math.018"].height = 100.0

    shader_nodetree.nodes["Math.019"].width  = 140.0
    shader_nodetree.nodes["Math.019"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate.003"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate.003"].height = 100.0

    shader_nodetree.nodes["Combine XYZ.003"].width  = 140.0
    shader_nodetree.nodes["Combine XYZ.003"].height = 100.0

    shader_nodetree.nodes["X_Tiles"].width  = 140.0
    shader_nodetree.nodes["X_Tiles"].height = 100.0

    shader_nodetree.nodes["Y_Tiles"].width  = 140.0
    shader_nodetree.nodes["Y_Tiles"].height = 100.0

    shader_nodetree.nodes["Math.001"].width  = 140.0
    shader_nodetree.nodes["Math.001"].height = 100.0

    shader_nodetree.nodes["Math.002"].width  = 140.0
    shader_nodetree.nodes["Math.002"].height = 100.0

    shader_nodetree.nodes["Math.003"].width  = 140.0
    shader_nodetree.nodes["Math.003"].height = 100.0

    shader_nodetree.nodes["Math.010"].width  = 140.0
    shader_nodetree.nodes["Math.010"].height = 100.0

    shader_nodetree.nodes["Math.004"].width  = 140.0
    shader_nodetree.nodes["Math.004"].height = 100.0

    shader_nodetree.nodes["Math.012"].width  = 140.0
    shader_nodetree.nodes["Math.012"].height = 100.0

    shader_nodetree.nodes["Math.015"].width  = 140.0
    shader_nodetree.nodes["Math.015"].height = 100.0

    shader_nodetree.nodes["Math.005"].width  = 140.0
    shader_nodetree.nodes["Math.005"].height = 100.0

    shader_nodetree.nodes["Math.020"].width  = 140.0
    shader_nodetree.nodes["Math.020"].height = 100.0

    shader_nodetree.nodes["Math.021"].width  = 134.2275390625
    shader_nodetree.nodes["Math.021"].height = 100.0

    shader_nodetree.nodes["Math.022"].width  = 140.0
    shader_nodetree.nodes["Math.022"].height = 100.0

    shader_nodetree.nodes["Math.023"].width  = 140.0
    shader_nodetree.nodes["Math.023"].height = 100.0

    shader_nodetree.nodes["Math.008"].width  = 140.0
    shader_nodetree.nodes["Math.008"].height = 100.0


    # Initialize shader_nodetree links

    # pitch_000.Value -> center_000.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch.000"].outputs[0],
        shader_nodetree.nodes["Center.000"].inputs[0]
    )
    # math_006.Value -> x_tiles_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["X_Tiles.001"].inputs[0]
    )
    # math_006.Value -> x_tiles_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.006"].outputs[0],
        shader_nodetree.nodes["X_Tiles.002"].inputs[0]
    )
    # x_tiles_002.Value -> math_009.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.002"].outputs[0],
        shader_nodetree.nodes["Math.009"].inputs[0]
    )
    # x_tiles_001.Value -> combine_xyz.X
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
    # emission.Emission -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # tiles_vector.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tiles_Vector"].outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # vector_math_001.Vector -> tiles_vector.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.001"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector"].inputs[0]
    )
    # pitch_001.Value -> center_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch.001"].outputs[0],
        shader_nodetree.nodes["Center.001"].inputs[0]
    )
    # total_tiles_001.Value -> math_007.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Total_Tiles.001"].outputs[0],
        shader_nodetree.nodes["Math.007"].inputs[0]
    )
    # math_007.Value -> x_tiles_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["X_Tiles.003"].inputs[0]
    )
    # math_007.Value -> x_tiles_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.007"].outputs[0],
        shader_nodetree.nodes["X_Tiles.004"].inputs[0]
    )
    # x_tiles_004.Value -> math_011.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.004"].outputs[0],
        shader_nodetree.nodes["Math.011"].inputs[0]
    )
    # x_tiles_003.Value -> combine_xyz_001.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.003"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.001"].inputs[0]
    )
    # math_011.Value -> combine_xyz_001.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.011"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.001"].inputs[1]
    )
    # combine_xyz_001.Vector -> vector_math_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.001"].outputs[0],
        shader_nodetree.nodes["Vector Math.002"].inputs[0]
    )
    # tiles_vector_001.Vector -> image_texture_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tiles_Vector.001"].outputs[0],
        shader_nodetree.nodes["Image Texture.001"].inputs[0]
    )
    # vector_math_002.Vector -> tiles_vector_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.002"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector.001"].inputs[0]
    )
    # image_texture.Color -> separate_color.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Separate Color"].inputs[0]
    )
    # separate_color.Red -> combine_color.Red
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate Color"].outputs[0],
        shader_nodetree.nodes["Combine Color"].inputs[0]
    )
    # image_texture_001.Color -> separate_color_001.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.001"].outputs[0],
        shader_nodetree.nodes["Separate Color.001"].inputs[0]
    )
    # math.Value -> pitch_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math"].outputs[0],
        shader_nodetree.nodes["Pitch.001"].inputs[0]
    )
    # pitch_002.Value -> center_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch.002"].outputs[0],
        shader_nodetree.nodes["Center.002"].inputs[0]
    )
    # total_tiles_002.Value -> math_013.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Total_Tiles.002"].outputs[0],
        shader_nodetree.nodes["Math.013"].inputs[0]
    )
    # math_013.Value -> x_tiles_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.013"].outputs[0],
        shader_nodetree.nodes["X_Tiles.005"].inputs[0]
    )
    # math_013.Value -> x_tiles_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.013"].outputs[0],
        shader_nodetree.nodes["X_Tiles.006"].inputs[0]
    )
    # x_tiles_006.Value -> math_014.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.006"].outputs[0],
        shader_nodetree.nodes["Math.014"].inputs[0]
    )
    # x_tiles_005.Value -> combine_xyz_002.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles.005"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.002"].inputs[0]
    )
    # math_014.Value -> combine_xyz_002.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.014"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.002"].inputs[1]
    )
    # combine_xyz_002.Vector -> vector_math_003.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.002"].outputs[0],
        shader_nodetree.nodes["Vector Math.003"].inputs[0]
    )
    # tiles_vector_002.Vector -> image_texture_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tiles_Vector.002"].outputs[0],
        shader_nodetree.nodes["Image Texture.002"].inputs[0]
    )
    # vector_math_003.Vector -> tiles_vector_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Vector Math.003"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector.002"].inputs[0]
    )
    # math_016.Value -> pitch_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.016"].outputs[0],
        shader_nodetree.nodes["Pitch.002"].inputs[0]
    )
    # texture_coordinate_001.UV -> vector_math_003.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate.001"].outputs[2],
        shader_nodetree.nodes["Vector Math.003"].inputs[1]
    )
    # subpixel.Value -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Subpixel"].outputs[0],
        shader_nodetree.nodes["Math"].inputs[1]
    )
    # separate_color_001.Green -> combine_color.Green
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate Color.001"].outputs[1],
        shader_nodetree.nodes["Combine Color"].inputs[1]
    )
    # subpixel.Value -> math_017.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Subpixel"].outputs[0],
        shader_nodetree.nodes["Math.017"].inputs[0]
    )
    # math_017.Value -> math_016.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.017"].outputs[0],
        shader_nodetree.nodes["Math.016"].inputs[1]
    )
    # image_texture_002.Color -> separate_color_002.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.002"].outputs[0],
        shader_nodetree.nodes["Separate Color.002"].inputs[0]
    )
    # separate_color_002.Blue -> combine_color.Blue
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate Color.002"].outputs[2],
        shader_nodetree.nodes["Combine Color"].inputs[2]
    )
    # pitch.Value -> pitch_000.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch"].outputs[0],
        shader_nodetree.nodes["Pitch.000"].inputs[1]
    )
    # pitch.Value -> pitch_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch"].outputs[0],
        shader_nodetree.nodes["Pitch.001"].inputs[1]
    )
    # pitch.Value -> pitch_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Pitch"].outputs[0],
        shader_nodetree.nodes["Pitch.002"].inputs[1]
    )
    # center.Value -> center_000.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center"].outputs[0],
        shader_nodetree.nodes["Center.000"].inputs[1]
    )
    # center.Value -> center_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center"].outputs[0],
        shader_nodetree.nodes["Center.001"].inputs[1]
    )
    # center.Value -> center_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center"].outputs[0],
        shader_nodetree.nodes["Center.002"].inputs[1]
    )
    # texture_coordinate_002.UV -> separate_xyz_003.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate.002"].outputs[2],
        shader_nodetree.nodes["Separate XYZ.003"].inputs[0]
    )
    # separate_xyz_003.Y -> tilt_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.003"].outputs[1],
        shader_nodetree.nodes["Tilt.003"].inputs[0]
    )
    # tilt_003.Value -> math_018.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tilt.003"].outputs[0],
        shader_nodetree.nodes["Math.018"].inputs[1]
    )
    # separate_xyz_003.X -> math_019.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Separate XYZ.003"].outputs[0],
        shader_nodetree.nodes["Math.019"].inputs[1]
    )
    # math_019.Value -> math_018.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.019"].outputs[0],
        shader_nodetree.nodes["Math.018"].inputs[0]
    )
    # tilt.Value -> tilt_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Tilt"].outputs[0],
        shader_nodetree.nodes["Tilt.003"].inputs[1]
    )
    # math_018.Value -> pitch_000.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.018"].outputs[0],
        shader_nodetree.nodes["Pitch.000"].inputs[0]
    )
    # math_018.Value -> math.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.018"].outputs[0],
        shader_nodetree.nodes["Math"].inputs[0]
    )
    # math_018.Value -> math_016.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.018"].outputs[0],
        shader_nodetree.nodes["Math.016"].inputs[0]
    )
    # texture_coordinate_003.UV -> vector_math_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate.003"].outputs[2],
        shader_nodetree.nodes["Vector Math.002"].inputs[1]
    )
    # x_tiles.Value -> combine_xyz_003.X
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.003"].inputs[0]
    )
    # y_tiles.Value -> combine_xyz_003.Y
    shader_nodetree.links.new(
        shader_nodetree.nodes["Y_Tiles"].outputs[0],
        shader_nodetree.nodes["Combine XYZ.003"].inputs[1]
    )
    # x_tiles.Value -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[0]
    )
    # y_tiles.Value -> math_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Y_Tiles"].outputs[0],
        shader_nodetree.nodes["Math.001"].inputs[1]
    )
    # math_001.Value -> total_tiles.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Total_Tiles"].inputs[1]
    )
    # math_001.Value -> total_tiles_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Total_Tiles.001"].inputs[1]
    )
    # math_001.Value -> total_tiles_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.001"].outputs[0],
        shader_nodetree.nodes["Total_Tiles.002"].inputs[1]
    )
    # combine_xyz_003.Vector -> tiles_vector.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.003"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector"].inputs[1]
    )
    # combine_xyz_003.Vector -> tiles_vector_001.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.003"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector.001"].inputs[1]
    )
    # combine_xyz_003.Vector -> tiles_vector_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine XYZ.003"].outputs[0],
        shader_nodetree.nodes["Tiles_Vector.002"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.001"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.002"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.003"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.004"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.005"].inputs[1]
    )
    # x_tiles.Value -> x_tiles_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["X_Tiles"].outputs[0],
        shader_nodetree.nodes["X_Tiles.006"].inputs[1]
    )
    # total_tiles.Value -> math_006.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Total_Tiles"].outputs[0],
        shader_nodetree.nodes["Math.006"].inputs[0]
    )
    # center_000.Value -> math_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.000"].outputs[0],
        shader_nodetree.nodes["Math.002"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.002"].outputs[0],
        shader_nodetree.nodes["Math.003"].inputs[0]
    )
    # math_003.Value -> math_010.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.003"].outputs[0],
        shader_nodetree.nodes["Math.010"].inputs[0]
    )
    # center_000.Value -> math_010.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.000"].outputs[0],
        shader_nodetree.nodes["Math.010"].inputs[1]
    )
    # math_004.Value -> math_012.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.004"].outputs[0],
        shader_nodetree.nodes["Math.012"].inputs[0]
    )
    # math_012.Value -> math_015.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.012"].outputs[0],
        shader_nodetree.nodes["Math.015"].inputs[0]
    )
    # center_001.Value -> math_004.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.001"].outputs[0],
        shader_nodetree.nodes["Math.004"].inputs[0]
    )
    # math_022.Value -> total_tiles_001.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.022"].outputs[0],
        shader_nodetree.nodes["Total_Tiles.001"].inputs[0]
    )
    # math_005.Value -> math_020.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.005"].outputs[0],
        shader_nodetree.nodes["Math.020"].inputs[0]
    )
    # math_020.Value -> math_021.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.020"].outputs[0],
        shader_nodetree.nodes["Math.021"].inputs[0]
    )
    # center_002.Value -> math_005.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.002"].outputs[0],
        shader_nodetree.nodes["Math.005"].inputs[0]
    )
    # center_001.Value -> math_015.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.001"].outputs[0],
        shader_nodetree.nodes["Math.015"].inputs[1]
    )
    # center_002.Value -> math_021.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Center.002"].outputs[0],
        shader_nodetree.nodes["Math.021"].inputs[1]
    )
    # math_023.Value -> total_tiles_002.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.023"].outputs[0],
        shader_nodetree.nodes["Total_Tiles.002"].inputs[0]
    )
    # combine_color.Color -> emission.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Combine Color"].outputs[0],
        shader_nodetree.nodes["Emission"].inputs[0]
    )
    # math_015.Value -> math_022.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.015"].outputs[0],
        shader_nodetree.nodes["Math.022"].inputs[0]
    )
    # math_021.Value -> math_023.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.021"].outputs[0],
        shader_nodetree.nodes["Math.023"].inputs[0]
    )
    # math_008.Value -> total_tiles.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.008"].outputs[0],
        shader_nodetree.nodes["Total_Tiles"].inputs[0]
    )
    # math_010.Value -> math_008.Value
    shader_nodetree.links.new(
        shader_nodetree.nodes["Math.010"].outputs[0],
        shader_nodetree.nodes["Math.008"].inputs[0]
    )

    return lkg_mat
