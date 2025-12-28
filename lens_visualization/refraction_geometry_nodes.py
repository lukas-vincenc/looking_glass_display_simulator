import bpy
import typing


def nodegroup_1_node_group():
    """Initialize NodeGroup node group"""
    nodegroup_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="NodeGroup")

    nodegroup_1.color_tag = 'NONE'
    nodegroup_1.description = ""
    nodegroup_1.default_group_node_width = 140

    # nodegroup_1 interface

    # Socket Geometry
    geometry_socket = nodegroup_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Hit Position
    hit_position_socket = nodegroup_1.interface.new_socket(name="Hit Position", in_out='OUTPUT', socket_type='NodeSocketVector')
    hit_position_socket.default_value = (0.0, 0.0, 0.0)
    hit_position_socket.min_value = -3.4028234663852886e+38
    hit_position_socket.max_value = 3.4028234663852886e+38
    hit_position_socket.subtype = 'NONE'
    hit_position_socket.attribute_domain = 'POINT'
    hit_position_socket.default_input = 'VALUE'
    hit_position_socket.structure_type = 'AUTO'

    # Socket Hit Normal
    hit_normal_socket = nodegroup_1.interface.new_socket(name="Hit Normal", in_out='OUTPUT', socket_type='NodeSocketVector')
    hit_normal_socket.default_value = (0.0, 0.0, 0.0)
    hit_normal_socket.min_value = -3.4028234663852886e+38
    hit_normal_socket.max_value = 3.4028234663852886e+38
    hit_normal_socket.subtype = 'NONE'
    hit_normal_socket.attribute_domain = 'POINT'
    hit_normal_socket.default_input = 'VALUE'
    hit_normal_socket.structure_type = 'AUTO'

    # Socket Vector
    vector_socket = nodegroup_1.interface.new_socket(name="Vector", in_out='OUTPUT', socket_type='NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'
    vector_socket.default_input = 'VALUE'
    vector_socket.structure_type = 'AUTO'

    # Socket Incoming
    incoming_socket = nodegroup_1.interface.new_socket(name="Incoming", in_out='INPUT', socket_type='NodeSocketVector')
    incoming_socket.default_value = (0.0, 0.0, 0.0)
    incoming_socket.min_value = -10000.0
    incoming_socket.max_value = 10000.0
    incoming_socket.subtype = 'NONE'
    incoming_socket.attribute_domain = 'POINT'
    incoming_socket.default_input = 'VALUE'
    incoming_socket.structure_type = 'AUTO'

    # Socket Normal
    normal_socket = nodegroup_1.interface.new_socket(name="Normal", in_out='INPUT', socket_type='NodeSocketVector')
    normal_socket.default_value = (0.0, 0.0, 0.0)
    normal_socket.min_value = -10000.0
    normal_socket.max_value = 10000.0
    normal_socket.subtype = 'NONE'
    normal_socket.attribute_domain = 'POINT'
    normal_socket.default_input = 'VALUE'
    normal_socket.structure_type = 'AUTO'

    # Socket Target Geometry
    target_geometry_socket = nodegroup_1.interface.new_socket(name="Target Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    target_geometry_socket.attribute_domain = 'POINT'
    target_geometry_socket.default_input = 'VALUE'
    target_geometry_socket.structure_type = 'AUTO'

    # Socket Position
    position_socket = nodegroup_1.interface.new_socket(name="Position", in_out='INPUT', socket_type='NodeSocketVector')
    position_socket.default_value = (0.0, 0.0, 0.0)
    position_socket.min_value = -10000.0
    position_socket.max_value = 10000.0
    position_socket.subtype = 'NONE'
    position_socket.attribute_domain = 'POINT'
    position_socket.default_input = 'VALUE'
    position_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = nodegroup_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket Value
    value_socket = nodegroup_1.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketInt')
    value_socket.default_value = 0
    value_socket.min_value = -2147483648
    value_socket.max_value = 2147483647
    value_socket.subtype = 'NONE'
    value_socket.attribute_domain = 'POINT'
    value_socket.default_input = 'VALUE'
    value_socket.structure_type = 'AUTO'

    # Socket IOR
    ior_socket = nodegroup_1.interface.new_socket(name="IOR", in_out='INPUT', socket_type='NodeSocketFloat')
    ior_socket.default_value = 1.0000001192092896
    ior_socket.min_value = -10000.0
    ior_socket.max_value = 10000.0
    ior_socket.subtype = 'NONE'
    ior_socket.attribute_domain = 'POINT'
    ior_socket.default_input = 'VALUE'
    ior_socket.structure_type = 'AUTO'

    # Initialize nodegroup_1 nodes

    # Node Group Output
    group_output = nodegroup_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = nodegroup_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Raycast.001
    raycast_001 = nodegroup_1.nodes.new("GeometryNodeRaycast")
    raycast_001.name = "Raycast.001"
    raycast_001.data_type = 'FLOAT'
    raycast_001.mapping = 'INTERPOLATED'
    # Attribute
    raycast_001.inputs[1].default_value = 0.0
    # Ray Length
    raycast_001.inputs[4].default_value = 100.0

    # Node Vector Math.009
    vector_math_009 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'ADD'

    # Node Set Position.001
    set_position_001 = nodegroup_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Index.001
    index_001 = nodegroup_1.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.hide = True

    # Node Math.001
    math_001 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'GREATER_THAN'
    math_001.use_clamp = False

    # Node Math.002
    math_002 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'ADD'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 0.5

    # Node Vector Math.010
    vector_math_010 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'REFRACT'

    # Node Vector Math
    vector_math = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'

    # Node Math.003
    math_003 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MODULO'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 2.0

    # Node Mix
    mix = nodegroup_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'VECTOR'
    mix.factor_mode = 'UNIFORM'
    # A_Vector
    mix.inputs[4].default_value = (1.0, -1.0, 1.0)
    # B_Vector
    mix.inputs[5].default_value = (1.0, 1.0, 1.0)

    # Node Vector Math.001
    vector_math_001 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.hide = True
    vector_math_001.operation = 'NORMALIZE'

    # Node Vector Math.002
    vector_math_002 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.hide = True
    vector_math_002.operation = 'NORMALIZE'

    # Node Vector Math.003
    vector_math_003 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.hide = True
    vector_math_003.operation = 'DOT_PRODUCT'

    # Node Math.004
    math_004 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'POWER'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 2.0

    # Node Math.005
    math_005 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'POWER'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = 2.0

    # Node Math.006
    math_006 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'SUBTRACT'
    math_006.use_clamp = False
    # Value
    math_006.inputs[0].default_value = 1.0

    # Node Math.007
    math_007 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.hide = True
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = False

    # Node Math.008
    math_008 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'SUBTRACT'
    math_008.use_clamp = False
    # Value
    math_008.inputs[0].default_value = 1.0

    # Node Group Input.001
    group_input_001 = nodegroup_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    # Node Math.009
    math_009 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.hide = True
    math_009.operation = 'SQRT'
    math_009.use_clamp = False

    # Node Math.010
    math_010 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.hide = True
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False

    # Node Math.011
    math_011 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.hide = True
    math_011.operation = 'SUBTRACT'
    math_011.use_clamp = False

    # Node Vector Math.004
    vector_math_004 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.hide = True
    vector_math_004.operation = 'MULTIPLY'

    # Node Group Input.002
    group_input_002 = nodegroup_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"

    # Node Vector Math.005
    vector_math_005 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.hide = True
    vector_math_005.operation = 'ADD'

    # Node Vector Math.006
    vector_math_006 = nodegroup_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.hide = True
    vector_math_006.operation = 'MULTIPLY'

    # Node Math.012
    math_012 = nodegroup_1.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.operation = 'MULTIPLY'
    math_012.use_clamp = False
    # Value_001
    math_012.inputs[1].default_value = -1.0

    # Node Switch
    switch = nodegroup_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    # Node Group Input.003
    group_input_003 = nodegroup_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.hide = True

    # Set locations
    nodegroup_1.nodes["Group Output"].location = (999.2705078125, -194.07225036621094)
    nodegroup_1.nodes["Group Input"].location = (-1984.1273193359375, 187.29580688476562)
    nodegroup_1.nodes["Raycast.001"].location = (-170.60565185546875, 79.91206359863281)
    nodegroup_1.nodes["Vector Math.009"].location = (-750.345947265625, -116.04122924804688)
    nodegroup_1.nodes["Set Position.001"].location = (195.33135986328125, 515.9879150390625)
    nodegroup_1.nodes["Index.001"].location = (-358.9630432128906, 321.79461669921875)
    nodegroup_1.nodes["Math.001"].location = (-123.86756896972656, 388.4984436035156)
    nodegroup_1.nodes["Math.002"].location = (-375.67529296875, 228.40689086914062)
    nodegroup_1.nodes["Vector Math.010"].location = (-1182.9439697265625, -216.77630615234375)
    nodegroup_1.nodes["Vector Math"].location = (-934.2550659179688, -295.4033203125)
    nodegroup_1.nodes["Math.003"].location = (-1370.7099609375, -496.2256164550781)
    nodegroup_1.nodes["Mix"].location = (-1183.5499267578125, -399.62841796875)
    nodegroup_1.nodes["Vector Math.001"].location = (-1808.164794921875, -994.9264526367188)
    nodegroup_1.nodes["Vector Math.002"].location = (-1810.8717041015625, -1060.9267578125)
    nodegroup_1.nodes["Vector Math.003"].location = (-1629.9503173828125, -1024.77197265625)
    nodegroup_1.nodes["Math.004"].location = (-1212.81103515625, -1220.179931640625)
    nodegroup_1.nodes["Math.005"].location = (-1213.5927734375, -1034.765625)
    nodegroup_1.nodes["Math.006"].location = (-989.4061279296875, -1027.198974609375)
    nodegroup_1.nodes["Math.007"].location = (-802.1400756835938, -1193.57958984375)
    nodegroup_1.nodes["Math.008"].location = (-620.885009765625, -1106.01904296875)
    nodegroup_1.nodes["Group Input.001"].location = (-2105.1103515625, -1136.850830078125)
    nodegroup_1.nodes["Math.009"].location = (-402.4231872558594, -1265.3885498046875)
    nodegroup_1.nodes["Math.010"].location = (-1212.1776123046875, -1461.3662109375)
    nodegroup_1.nodes["Math.011"].location = (-201.8746337890625, -1352.3372802734375)
    nodegroup_1.nodes["Vector Math.004"].location = (140.45396423339844, -1717.540283203125)
    nodegroup_1.nodes["Group Input.002"].location = (-592.7059326171875, -1685.1065673828125)
    nodegroup_1.nodes["Vector Math.005"].location = (395.3565979003906, -1694.71923828125)
    nodegroup_1.nodes["Vector Math.006"].location = (134.86302185058594, -1629.5853271484375)
    nodegroup_1.nodes["Math.012"].location = (-1448.484619140625, -1001.3099975585938)
    nodegroup_1.nodes["Switch"].location = (706.4102783203125, 296.622314453125)
    nodegroup_1.nodes["Group Input.003"].location = (463.76776123046875, 133.82357788085938)

    # Set dimensions
    nodegroup_1.nodes["Group Output"].width  = 140.0
    nodegroup_1.nodes["Group Output"].height = 100.0

    nodegroup_1.nodes["Group Input"].width  = 140.0
    nodegroup_1.nodes["Group Input"].height = 100.0

    nodegroup_1.nodes["Raycast.001"].width  = 150.0
    nodegroup_1.nodes["Raycast.001"].height = 100.0

    nodegroup_1.nodes["Vector Math.009"].width  = 140.0
    nodegroup_1.nodes["Vector Math.009"].height = 100.0

    nodegroup_1.nodes["Set Position.001"].width  = 140.0
    nodegroup_1.nodes["Set Position.001"].height = 100.0

    nodegroup_1.nodes["Index.001"].width  = 140.0
    nodegroup_1.nodes["Index.001"].height = 100.0

    nodegroup_1.nodes["Math.001"].width  = 140.0
    nodegroup_1.nodes["Math.001"].height = 100.0

    nodegroup_1.nodes["Math.002"].width  = 140.0
    nodegroup_1.nodes["Math.002"].height = 100.0

    nodegroup_1.nodes["Vector Math.010"].width  = 140.0
    nodegroup_1.nodes["Vector Math.010"].height = 100.0

    nodegroup_1.nodes["Vector Math"].width  = 140.0
    nodegroup_1.nodes["Vector Math"].height = 100.0

    nodegroup_1.nodes["Math.003"].width  = 140.0
    nodegroup_1.nodes["Math.003"].height = 100.0

    nodegroup_1.nodes["Mix"].width  = 140.0
    nodegroup_1.nodes["Mix"].height = 100.0

    nodegroup_1.nodes["Vector Math.001"].width  = 140.0
    nodegroup_1.nodes["Vector Math.001"].height = 100.0

    nodegroup_1.nodes["Vector Math.002"].width  = 140.0
    nodegroup_1.nodes["Vector Math.002"].height = 100.0

    nodegroup_1.nodes["Vector Math.003"].width  = 140.0
    nodegroup_1.nodes["Vector Math.003"].height = 100.0

    nodegroup_1.nodes["Math.004"].width  = 140.0
    nodegroup_1.nodes["Math.004"].height = 100.0

    nodegroup_1.nodes["Math.005"].width  = 140.0
    nodegroup_1.nodes["Math.005"].height = 100.0

    nodegroup_1.nodes["Math.006"].width  = 140.0
    nodegroup_1.nodes["Math.006"].height = 100.0

    nodegroup_1.nodes["Math.007"].width  = 140.0
    nodegroup_1.nodes["Math.007"].height = 100.0

    nodegroup_1.nodes["Math.008"].width  = 140.0
    nodegroup_1.nodes["Math.008"].height = 100.0

    nodegroup_1.nodes["Group Input.001"].width  = 140.0
    nodegroup_1.nodes["Group Input.001"].height = 100.0

    nodegroup_1.nodes["Math.009"].width  = 140.0
    nodegroup_1.nodes["Math.009"].height = 100.0

    nodegroup_1.nodes["Math.010"].width  = 140.0
    nodegroup_1.nodes["Math.010"].height = 100.0

    nodegroup_1.nodes["Math.011"].width  = 140.0
    nodegroup_1.nodes["Math.011"].height = 100.0

    nodegroup_1.nodes["Vector Math.004"].width  = 140.0
    nodegroup_1.nodes["Vector Math.004"].height = 100.0

    nodegroup_1.nodes["Group Input.002"].width  = 140.0
    nodegroup_1.nodes["Group Input.002"].height = 100.0

    nodegroup_1.nodes["Vector Math.005"].width  = 140.0
    nodegroup_1.nodes["Vector Math.005"].height = 100.0

    nodegroup_1.nodes["Vector Math.006"].width  = 140.0
    nodegroup_1.nodes["Vector Math.006"].height = 100.0

    nodegroup_1.nodes["Math.012"].width  = 140.0
    nodegroup_1.nodes["Math.012"].height = 100.0

    nodegroup_1.nodes["Switch"].width  = 140.0
    nodegroup_1.nodes["Switch"].height = 100.0

    nodegroup_1.nodes["Group Input.003"].width  = 140.0
    nodegroup_1.nodes["Group Input.003"].height = 100.0


    # Initialize nodegroup_1 links

    # raycast_001.Hit Position -> set_position_001.Position
    nodegroup_1.links.new(
        nodegroup_1.nodes["Raycast.001"].outputs[1],
        nodegroup_1.nodes["Set Position.001"].inputs[2]
    )
    # math_002.Value -> math_001.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.002"].outputs[0],
        nodegroup_1.nodes["Math.001"].inputs[1]
    )
    # index_001.Index -> math_001.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Index.001"].outputs[0],
        nodegroup_1.nodes["Math.001"].inputs[0]
    )
    # group_input.Target Geometry -> raycast_001.Target Geometry
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[2],
        nodegroup_1.nodes["Raycast.001"].inputs[0]
    )
    # group_input.Geometry -> set_position_001.Geometry
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[4],
        nodegroup_1.nodes["Set Position.001"].inputs[0]
    )
    # group_input.Position -> vector_math_009.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[3],
        nodegroup_1.nodes["Vector Math.009"].inputs[0]
    )
    # group_input.Value -> math_002.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[5],
        nodegroup_1.nodes["Math.002"].inputs[0]
    )
    # vector_math_009.Vector -> raycast_001.Source Position
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.009"].outputs[0],
        nodegroup_1.nodes["Raycast.001"].inputs[2]
    )
    # raycast_001.Hit Position -> group_output.Hit Position
    nodegroup_1.links.new(
        nodegroup_1.nodes["Raycast.001"].outputs[1],
        nodegroup_1.nodes["Group Output"].inputs[1]
    )
    # raycast_001.Hit Normal -> group_output.Hit Normal
    nodegroup_1.links.new(
        nodegroup_1.nodes["Raycast.001"].outputs[2],
        nodegroup_1.nodes["Group Output"].inputs[2]
    )
    # group_input.Incoming -> vector_math_010.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[0],
        nodegroup_1.nodes["Vector Math.010"].inputs[0]
    )
    # group_input.Normal -> vector_math_010.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[1],
        nodegroup_1.nodes["Vector Math.010"].inputs[1]
    )
    # group_input.IOR -> vector_math_010.Scale
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[6],
        nodegroup_1.nodes["Vector Math.010"].inputs[3]
    )
    # vector_math.Vector -> raycast_001.Ray Direction
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math"].outputs[0],
        nodegroup_1.nodes["Raycast.001"].inputs[3]
    )
    # vector_math.Vector -> group_output.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math"].outputs[0],
        nodegroup_1.nodes["Group Output"].inputs[3]
    )
    # vector_math.Vector -> vector_math_009.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math"].outputs[0],
        nodegroup_1.nodes["Vector Math.009"].inputs[1]
    )
    # math_001.Value -> set_position_001.Selection
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.001"].outputs[0],
        nodegroup_1.nodes["Set Position.001"].inputs[1]
    )
    # math_003.Value -> mix.Factor
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.003"].outputs[0],
        nodegroup_1.nodes["Mix"].inputs[0]
    )
    # mix.Result -> vector_math.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Mix"].outputs[1],
        nodegroup_1.nodes["Vector Math"].inputs[1]
    )
    # vector_math_001.Vector -> vector_math_003.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.001"].outputs[0],
        nodegroup_1.nodes["Vector Math.003"].inputs[0]
    )
    # vector_math_002.Vector -> vector_math_003.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.002"].outputs[0],
        nodegroup_1.nodes["Vector Math.003"].inputs[1]
    )
    # math_005.Value -> math_006.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.005"].outputs[0],
        nodegroup_1.nodes["Math.006"].inputs[1]
    )
    # math_006.Value -> math_007.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.006"].outputs[0],
        nodegroup_1.nodes["Math.007"].inputs[0]
    )
    # math_004.Value -> math_007.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.004"].outputs[0],
        nodegroup_1.nodes["Math.007"].inputs[1]
    )
    # math_007.Value -> math_008.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.007"].outputs[0],
        nodegroup_1.nodes["Math.008"].inputs[1]
    )
    # group_input_001.Incoming -> vector_math_001.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.001"].outputs[0],
        nodegroup_1.nodes["Vector Math.001"].inputs[0]
    )
    # group_input_001.Normal -> vector_math_002.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.001"].outputs[1],
        nodegroup_1.nodes["Vector Math.002"].inputs[0]
    )
    # group_input_001.IOR -> math_004.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.001"].outputs[6],
        nodegroup_1.nodes["Math.004"].inputs[0]
    )
    # math_008.Value -> math_009.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.008"].outputs[0],
        nodegroup_1.nodes["Math.009"].inputs[0]
    )
    # group_input_001.IOR -> math_010.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.001"].outputs[6],
        nodegroup_1.nodes["Math.010"].inputs[1]
    )
    # math_010.Value -> math_011.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.010"].outputs[0],
        nodegroup_1.nodes["Math.011"].inputs[0]
    )
    # math_009.Value -> math_011.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.009"].outputs[0],
        nodegroup_1.nodes["Math.011"].inputs[1]
    )
    # group_input_002.Incoming -> vector_math_004.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.002"].outputs[0],
        nodegroup_1.nodes["Vector Math.004"].inputs[1]
    )
    # group_input_002.IOR -> vector_math_004.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.002"].outputs[6],
        nodegroup_1.nodes["Vector Math.004"].inputs[0]
    )
    # vector_math_004.Vector -> vector_math_005.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.004"].outputs[0],
        nodegroup_1.nodes["Vector Math.005"].inputs[1]
    )
    # math_011.Value -> vector_math_006.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.011"].outputs[0],
        nodegroup_1.nodes["Vector Math.006"].inputs[0]
    )
    # group_input_002.Normal -> vector_math_006.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.002"].outputs[1],
        nodegroup_1.nodes["Vector Math.006"].inputs[1]
    )
    # vector_math_006.Vector -> vector_math_005.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.006"].outputs[0],
        nodegroup_1.nodes["Vector Math.005"].inputs[0]
    )
    # vector_math_003.Value -> math_012.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.003"].outputs[1],
        nodegroup_1.nodes["Math.012"].inputs[0]
    )
    # math_012.Value -> math_005.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.012"].outputs[0],
        nodegroup_1.nodes["Math.005"].inputs[0]
    )
    # math_012.Value -> math_010.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Math.012"].outputs[0],
        nodegroup_1.nodes["Math.010"].inputs[0]
    )
    # vector_math_005.Vector -> vector_math.Vector
    nodegroup_1.links.new(
        nodegroup_1.nodes["Vector Math.005"].outputs[0],
        nodegroup_1.nodes["Vector Math"].inputs[0]
    )
    # group_input.Value -> math_003.Value
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input"].outputs[5],
        nodegroup_1.nodes["Math.003"].inputs[0]
    )
    # raycast_001.Is Hit -> switch.Switch
    nodegroup_1.links.new(
        nodegroup_1.nodes["Raycast.001"].outputs[0],
        nodegroup_1.nodes["Switch"].inputs[0]
    )
    # set_position_001.Geometry -> switch.True
    nodegroup_1.links.new(
        nodegroup_1.nodes["Set Position.001"].outputs[0],
        nodegroup_1.nodes["Switch"].inputs[2]
    )
    # switch.Output -> group_output.Geometry
    nodegroup_1.links.new(
        nodegroup_1.nodes["Switch"].outputs[0],
        nodegroup_1.nodes["Group Output"].inputs[0]
    )
    # group_input_003.Geometry -> switch.False
    nodegroup_1.links.new(
        nodegroup_1.nodes["Group Input.003"].outputs[4],
        nodegroup_1.nodes["Switch"].inputs[1]
    )

    return nodegroup_1


def geometry_nodes_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Geometry Nodes node group"""
    geometry_nodes_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Geometry Nodes")

    geometry_nodes_1.color_tag = 'NONE'
    geometry_nodes_1.description = ""
    geometry_nodes_1.default_group_node_width = 140
    geometry_nodes_1.is_modifier = True

    # geometry_nodes_1 interface

    # Socket Geometry
    geometry_socket = geometry_nodes_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = geometry_nodes_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket Object
    object_socket = geometry_nodes_1.interface.new_socket(name="Object", in_out='INPUT', socket_type='NodeSocketObject')
    object_socket.attribute_domain = 'POINT'
    object_socket.default_input = 'VALUE'
    object_socket.structure_type = 'AUTO'

    # Socket Collection
    collection_socket = geometry_nodes_1.interface.new_socket(name="Collection", in_out='INPUT', socket_type='NodeSocketCollection')
    collection_socket.attribute_domain = 'POINT'
    collection_socket.default_input = 'VALUE'
    collection_socket.structure_type = 'AUTO'

    # Socket Radius
    radius_socket = geometry_nodes_1.interface.new_socket(name="Radius", in_out='INPUT', socket_type='NodeSocketFloat')
    radius_socket.default_value = 0.05000000074505806
    radius_socket.min_value = 0.0
    radius_socket.max_value = 3.4028234663852886e+38
    radius_socket.subtype = 'DISTANCE'
    radius_socket.attribute_domain = 'POINT'
    radius_socket.description = "Distance of the points from the origin"
    radius_socket.default_input = 'VALUE'
    radius_socket.structure_type = 'AUTO'

    # Initialize geometry_nodes_1 nodes

    # Node Group Input
    group_input = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Group Output
    group_output = geometry_nodes_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Mesh Line
    mesh_line = geometry_nodes_1.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'OFFSET'
    # Count
    mesh_line.inputs[0].default_value = 10
    # Offset
    mesh_line.inputs[3].default_value = (0.0, 0.0, 1.0)

    # Node Object Info
    object_info = geometry_nodes_1.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    # As Instance
    object_info.inputs[1].default_value = False

    # Node Collection Info
    collection_info = geometry_nodes_1.nodes.new("GeometryNodeCollectionInfo")
    collection_info.name = "Collection Info"
    collection_info.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info.inputs[1].default_value = False
    # Reset Children
    collection_info.inputs[2].default_value = False

    # Node Raycast
    raycast = geometry_nodes_1.nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.data_type = 'FLOAT'
    raycast.mapping = 'INTERPOLATED'
    # Attribute
    raycast.inputs[1].default_value = 0.0
    # Ray Length
    raycast.inputs[4].default_value = 100.0

    # Node Vector Rotate
    vector_rotate = geometry_nodes_1.nodes.new("ShaderNodeVectorRotate")
    vector_rotate.name = "Vector Rotate"
    vector_rotate.invert = False
    vector_rotate.rotation_type = 'EULER_XYZ'
    # Center
    vector_rotate.inputs[1].default_value = (0.0, 0.0, 0.0)

    # Node Vector
    vector = geometry_nodes_1.nodes.new("FunctionNodeInputVector")
    vector.name = "Vector"
    vector.vector = (1.0, 0.0, 0.0)

    # Node Realize Instances
    realize_instances = geometry_nodes_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.hide = True
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Node Set Position
    set_position = geometry_nodes_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Math
    math = geometry_nodes_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'GREATER_THAN'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 0.5

    # Node Index
    index = geometry_nodes_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Mesh to Curve
    mesh_to_curve = geometry_nodes_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.mode = 'EDGES'
    # Selection
    mesh_to_curve.inputs[1].default_value = True

    # Node Curve to Mesh
    curve_to_mesh = geometry_nodes_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False

    # Node Curve Circle
    curve_circle = geometry_nodes_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 8

    # Node Group Input.001
    group_input_001 = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    # Node Math.001
    math_001 = geometry_nodes_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 100.0

    # Node Repeat Input
    repeat_input = geometry_nodes_1.nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    # Node Repeat Output
    repeat_output = geometry_nodes_1.nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.active_index = 3
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.clear()
    # Create item "Geometry"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Hit Position"
    repeat_output.repeat_items.new('VECTOR', "Hit Position")
    # Create item "Hit Normal"
    repeat_output.repeat_items.new('VECTOR', "Hit Normal")
    # Create item "Vector"
    repeat_output.repeat_items.new('VECTOR', "Vector")

    # Node Group.002
    group_002 = geometry_nodes_1.nodes.new("GeometryNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = bpy.data.node_groups[node_tree_names[nodegroup_1_node_group]]

    # Node Math.002
    math_002 = geometry_nodes_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MODULO'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 2.0

    # Node Mix
    mix = geometry_nodes_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'FLOAT'
    mix.factor_mode = 'UNIFORM'
    # A_Float
    mix.inputs[2].default_value = 0.6710000038146973
    # B_Float
    mix.inputs[3].default_value = 1.4900000095367432

    # Node Math.003
    math_003 = geometry_nodes_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'ADD'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 1.0

    # Process zone input Repeat Input
    repeat_input.pair_with_output(repeat_output)
    # Iterations
    repeat_input.inputs[0].default_value = 2



    # Set locations
    geometry_nodes_1.nodes["Group Input"].location = (-1189.33837890625, -213.7196044921875)
    geometry_nodes_1.nodes["Group Output"].location = (2259.921875, -48.11536407470703)
    geometry_nodes_1.nodes["Mesh Line"].location = (-579.1228637695312, 242.66317749023438)
    geometry_nodes_1.nodes["Object Info"].location = (-881.355712890625, -84.12420654296875)
    geometry_nodes_1.nodes["Collection Info"].location = (-879.3777465820312, -338.4110412597656)
    geometry_nodes_1.nodes["Raycast"].location = (23.834779739379883, -70.794677734375)
    geometry_nodes_1.nodes["Vector Rotate"].location = (-375.02679443359375, -41.57830047607422)
    geometry_nodes_1.nodes["Vector"].location = (-579.7034301757812, -13.19308090209961)
    geometry_nodes_1.nodes["Realize Instances"].location = (-343.1776428222656, -471.8594665527344)
    geometry_nodes_1.nodes["Set Position"].location = (427.96826171875, 197.15115356445312)
    geometry_nodes_1.nodes["Math"].location = (46.833675384521484, 144.4937744140625)
    geometry_nodes_1.nodes["Index"].location = (-185.5345001220703, 71.98434448242188)
    geometry_nodes_1.nodes["Mesh to Curve"].location = (1855.990478515625, -73.84111785888672)
    geometry_nodes_1.nodes["Curve to Mesh"].location = (2082.084228515625, -45.867713928222656)
    geometry_nodes_1.nodes["Curve Circle"].location = (1892.4189453125, -301.54034423828125)
    geometry_nodes_1.nodes["Group Input.001"].location = (1517.3599853515625, -410.1059265136719)
    geometry_nodes_1.nodes["Math.001"].location = (1698.7220458984375, -402.3659973144531)
    geometry_nodes_1.nodes["Repeat Input"].location = (695.2578125, 82.60127258300781)
    geometry_nodes_1.nodes["Repeat Output"].location = (1542.8525390625, -115.24014282226562)
    geometry_nodes_1.nodes["Group.002"].location = (1332.514892578125, -118.73501586914062)
    geometry_nodes_1.nodes["Math.002"].location = (918.1700439453125, -439.06927490234375)
    geometry_nodes_1.nodes["Mix"].location = (1117.287353515625, -410.5)
    geometry_nodes_1.nodes["Math.003"].location = (934.309326171875, 162.8408966064453)

    # Set dimensions
    geometry_nodes_1.nodes["Group Input"].width  = 140.0
    geometry_nodes_1.nodes["Group Input"].height = 100.0

    geometry_nodes_1.nodes["Group Output"].width  = 140.0
    geometry_nodes_1.nodes["Group Output"].height = 100.0

    geometry_nodes_1.nodes["Mesh Line"].width  = 140.0
    geometry_nodes_1.nodes["Mesh Line"].height = 100.0

    geometry_nodes_1.nodes["Object Info"].width  = 140.0
    geometry_nodes_1.nodes["Object Info"].height = 100.0

    geometry_nodes_1.nodes["Collection Info"].width  = 140.0
    geometry_nodes_1.nodes["Collection Info"].height = 100.0

    geometry_nodes_1.nodes["Raycast"].width  = 150.0
    geometry_nodes_1.nodes["Raycast"].height = 100.0

    geometry_nodes_1.nodes["Vector Rotate"].width  = 140.0
    geometry_nodes_1.nodes["Vector Rotate"].height = 100.0

    geometry_nodes_1.nodes["Vector"].width  = 140.0
    geometry_nodes_1.nodes["Vector"].height = 100.0

    geometry_nodes_1.nodes["Realize Instances"].width  = 140.0
    geometry_nodes_1.nodes["Realize Instances"].height = 100.0

    geometry_nodes_1.nodes["Set Position"].width  = 140.0
    geometry_nodes_1.nodes["Set Position"].height = 100.0

    geometry_nodes_1.nodes["Math"].width  = 140.0
    geometry_nodes_1.nodes["Math"].height = 100.0

    geometry_nodes_1.nodes["Index"].width  = 140.0
    geometry_nodes_1.nodes["Index"].height = 100.0

    geometry_nodes_1.nodes["Mesh to Curve"].width  = 140.0
    geometry_nodes_1.nodes["Mesh to Curve"].height = 100.0

    geometry_nodes_1.nodes["Curve to Mesh"].width  = 140.0
    geometry_nodes_1.nodes["Curve to Mesh"].height = 100.0

    geometry_nodes_1.nodes["Curve Circle"].width  = 140.0
    geometry_nodes_1.nodes["Curve Circle"].height = 100.0

    geometry_nodes_1.nodes["Group Input.001"].width  = 140.0
    geometry_nodes_1.nodes["Group Input.001"].height = 100.0

    geometry_nodes_1.nodes["Math.001"].width  = 140.0
    geometry_nodes_1.nodes["Math.001"].height = 100.0

    geometry_nodes_1.nodes["Repeat Input"].width  = 140.0
    geometry_nodes_1.nodes["Repeat Input"].height = 100.0

    geometry_nodes_1.nodes["Repeat Output"].width  = 140.0
    geometry_nodes_1.nodes["Repeat Output"].height = 100.0

    geometry_nodes_1.nodes["Group.002"].width  = 140.0
    geometry_nodes_1.nodes["Group.002"].height = 100.0

    geometry_nodes_1.nodes["Math.002"].width  = 140.0
    geometry_nodes_1.nodes["Math.002"].height = 100.0

    geometry_nodes_1.nodes["Mix"].width  = 140.0
    geometry_nodes_1.nodes["Mix"].height = 100.0

    geometry_nodes_1.nodes["Math.003"].width  = 140.0
    geometry_nodes_1.nodes["Math.003"].height = 100.0


    # Initialize geometry_nodes_1 links

    # curve_to_mesh.Mesh -> group_output.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Curve to Mesh"].outputs[0],
        geometry_nodes_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Object -> object_info.Object
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input"].outputs[1],
        geometry_nodes_1.nodes["Object Info"].inputs[0]
    )
    # group_input.Collection -> collection_info.Collection
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input"].outputs[2],
        geometry_nodes_1.nodes["Collection Info"].inputs[0]
    )
    # object_info.Rotation -> vector_rotate.Rotation
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Object Info"].outputs[2],
        geometry_nodes_1.nodes["Vector Rotate"].inputs[4]
    )
    # vector.Vector -> vector_rotate.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector"].outputs[0],
        geometry_nodes_1.nodes["Vector Rotate"].inputs[0]
    )
    # vector_rotate.Vector -> raycast.Ray Direction
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Rotate"].outputs[0],
        geometry_nodes_1.nodes["Raycast"].inputs[3]
    )
    # collection_info.Instances -> realize_instances.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Collection Info"].outputs[0],
        geometry_nodes_1.nodes["Realize Instances"].inputs[0]
    )
    # realize_instances.Geometry -> raycast.Target Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Realize Instances"].outputs[0],
        geometry_nodes_1.nodes["Raycast"].inputs[0]
    )
    # mesh_line.Mesh -> set_position.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Mesh Line"].outputs[0],
        geometry_nodes_1.nodes["Set Position"].inputs[0]
    )
    # raycast.Hit Position -> set_position.Position
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Raycast"].outputs[1],
        geometry_nodes_1.nodes["Set Position"].inputs[2]
    )
    # object_info.Location -> raycast.Source Position
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Object Info"].outputs[1],
        geometry_nodes_1.nodes["Raycast"].inputs[2]
    )
    # index.Index -> math.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Index"].outputs[0],
        geometry_nodes_1.nodes["Math"].inputs[0]
    )
    # math.Value -> set_position.Selection
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Math"].outputs[0],
        geometry_nodes_1.nodes["Set Position"].inputs[1]
    )
    # object_info.Location -> mesh_line.Start Location
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Object Info"].outputs[1],
        geometry_nodes_1.nodes["Mesh Line"].inputs[2]
    )
    # mesh_to_curve.Curve -> curve_to_mesh.Curve
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Mesh to Curve"].outputs[0],
        geometry_nodes_1.nodes["Curve to Mesh"].inputs[0]
    )
    # curve_circle.Curve -> curve_to_mesh.Profile Curve
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Curve Circle"].outputs[0],
        geometry_nodes_1.nodes["Curve to Mesh"].inputs[1]
    )
    # math_001.Value -> curve_circle.Radius
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Math.001"].outputs[0],
        geometry_nodes_1.nodes["Curve Circle"].inputs[4]
    )
    # group_input_001.Radius -> math_001.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input.001"].outputs[3],
        geometry_nodes_1.nodes["Math.001"].inputs[0]
    )
    # raycast.Hit Position -> repeat_input.Hit Position
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Raycast"].outputs[1],
        geometry_nodes_1.nodes["Repeat Input"].inputs[2]
    )
    # set_position.Geometry -> repeat_input.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Set Position"].outputs[0],
        geometry_nodes_1.nodes["Repeat Input"].inputs[1]
    )
    # raycast.Hit Normal -> repeat_input.Hit Normal
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Raycast"].outputs[2],
        geometry_nodes_1.nodes["Repeat Input"].inputs[3]
    )
    # repeat_input.Hit Position -> group_002.Position
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[2],
        geometry_nodes_1.nodes["Group.002"].inputs[3]
    )
    # repeat_input.Hit Normal -> group_002.Normal
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[3],
        geometry_nodes_1.nodes["Group.002"].inputs[1]
    )
    # vector_rotate.Vector -> repeat_input.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Rotate"].outputs[0],
        geometry_nodes_1.nodes["Repeat Input"].inputs[4]
    )
    # repeat_input.Vector -> group_002.Incoming
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[4],
        geometry_nodes_1.nodes["Group.002"].inputs[0]
    )
    # realize_instances.Geometry -> group_002.Target Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Realize Instances"].outputs[0],
        geometry_nodes_1.nodes["Group.002"].inputs[2]
    )
    # repeat_input.Geometry -> group_002.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[1],
        geometry_nodes_1.nodes["Group.002"].inputs[4]
    )
    # math_003.Value -> group_002.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Math.003"].outputs[0],
        geometry_nodes_1.nodes["Group.002"].inputs[5]
    )
    # group_002.Hit Position -> repeat_output.Hit Position
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group.002"].outputs[1],
        geometry_nodes_1.nodes["Repeat Output"].inputs[1]
    )
    # group_002.Hit Normal -> repeat_output.Hit Normal
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group.002"].outputs[2],
        geometry_nodes_1.nodes["Repeat Output"].inputs[2]
    )
    # group_002.Vector -> repeat_output.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group.002"].outputs[3],
        geometry_nodes_1.nodes["Repeat Output"].inputs[3]
    )
    # repeat_input.Iteration -> math_002.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[0],
        geometry_nodes_1.nodes["Math.002"].inputs[0]
    )
    # math_002.Value -> mix.Factor
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Math.002"].outputs[0],
        geometry_nodes_1.nodes["Mix"].inputs[0]
    )
    # mix.Result -> group_002.IOR
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Mix"].outputs[0],
        geometry_nodes_1.nodes["Group.002"].inputs[6]
    )
    # repeat_input.Iteration -> math_003.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Input"].outputs[0],
        geometry_nodes_1.nodes["Math.003"].inputs[0]
    )
    # group_002.Geometry -> repeat_output.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group.002"].outputs[0],
        geometry_nodes_1.nodes["Repeat Output"].inputs[0]
    )
    # repeat_output.Geometry -> mesh_to_curve.Mesh
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Repeat Output"].outputs[0],
        geometry_nodes_1.nodes["Mesh to Curve"].inputs[0]
    )

    return geometry_nodes_1


def get_node_tree():
    # Maps node tree creation functions to the node tree
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names: dict[typing.Callable, str] = {}

    nodegroup = nodegroup_1_node_group()
    node_tree_names[nodegroup_1_node_group] = nodegroup.name

    geometry_nodes = geometry_nodes_1_node_group(node_tree_names)
    node_tree_names[geometry_nodes_1_node_group] = geometry_nodes.name

    return geometry_nodes
