import bpy
import typing


def get_node_tree():
    geometry_nodes_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Geometry Nodes.004")

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

    # Socket Pitch
    pitch_socket = geometry_nodes_1.interface.new_socket(name="Pitch", in_out='INPUT', socket_type='NodeSocketInt')
    pitch_socket.default_value = 355
    pitch_socket.min_value = 1
    pitch_socket.max_value = 10000
    pitch_socket.subtype = 'NONE'
    pitch_socket.attribute_domain = 'POINT'
    pitch_socket.description = "Number of vertices on the line"
    pitch_socket.default_input = 'VALUE'
    pitch_socket.structure_type = 'AUTO'

    # Socket Extra Lenses
    extra_lenses_socket = geometry_nodes_1.interface.new_socket(name="Extra Lenses", in_out='INPUT', socket_type='NodeSocketInt')
    extra_lenses_socket.default_value = 40
    extra_lenses_socket.min_value = 1
    extra_lenses_socket.max_value = 10000
    extra_lenses_socket.subtype = 'NONE'
    extra_lenses_socket.attribute_domain = 'POINT'
    extra_lenses_socket.description = "Number of vertices on the line"
    extra_lenses_socket.default_input = 'VALUE'
    extra_lenses_socket.structure_type = 'AUTO'

    # Initialize geometry_nodes_1 nodes

    # Node Group Input
    group_input = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Group Output
    group_output = geometry_nodes_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Instance on Points
    instance_on_points = geometry_nodes_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Mesh Line
    mesh_line = geometry_nodes_1.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'OFFSET'
    # Start Location
    mesh_line.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Bounding Box
    bounding_box = geometry_nodes_1.nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True

    # Node Vector Math
    vector_math = geometry_nodes_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'SUBTRACT'

    # Node Separate XYZ
    separate_xyz = geometry_nodes_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Combine XYZ
    combine_xyz = geometry_nodes_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Y
    combine_xyz.inputs[1].default_value = 0.0
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Vector Math.001
    vector_math_001 = geometry_nodes_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'
    # Vector_001
    vector_math_001.inputs[1].default_value = (9.999999974752427e-07, 0.0, 0.0)

    # Node Instance on Points.001
    instance_on_points_001 = geometry_nodes_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_001.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Mesh Line.001
    mesh_line_001 = geometry_nodes_1.nodes.new("GeometryNodeMeshLine")
    mesh_line_001.name = "Mesh Line.001"
    mesh_line_001.count_mode = 'TOTAL'
    mesh_line_001.mode = 'OFFSET'

    # Node Vector Math.002
    vector_math_002 = geometry_nodes_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'MULTIPLY'
    # Vector_001
    vector_math_002.inputs[1].default_value = (-1.0, 0.0, 0.0)

    # Node Join Geometry
    join_geometry = geometry_nodes_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # Node Group Input.001
    group_input_001 = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    # Node Group Input.002
    group_input_002 = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"

    # Node Group Input.003
    group_input_003 = geometry_nodes_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"

    # Node Math
    math = geometry_nodes_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'ABSOLUTE'
    math.use_clamp = False

    # Set locations
    geometry_nodes_1.nodes["Group Input"].location = (-786.2814331054688, 127.74369812011719)
    geometry_nodes_1.nodes["Group Output"].location = (1113.94580078125, -47.02090835571289)
    geometry_nodes_1.nodes["Instance on Points"].location = (675.4236450195312, 204.7719268798828)
    geometry_nodes_1.nodes["Mesh Line"].location = (292.9961853027344, 337.277099609375)
    geometry_nodes_1.nodes["Bounding Box"].location = (-614.9393310546875, 199.29164123535156)
    geometry_nodes_1.nodes["Vector Math"].location = (-434.49725341796875, 223.71035766601562)
    geometry_nodes_1.nodes["Separate XYZ"].location = (-263.810546875, 221.37921142578125)
    geometry_nodes_1.nodes["Combine XYZ"].location = (-99.90115356445312, 222.16078186035156)
    geometry_nodes_1.nodes["Vector Math.001"].location = (68.47270202636719, 218.3512420654297)
    geometry_nodes_1.nodes["Instance on Points.001"].location = (669.3336181640625, -270.4549255371094)
    geometry_nodes_1.nodes["Mesh Line.001"].location = (410.3204040527344, -234.2307586669922)
    geometry_nodes_1.nodes["Vector Math.002"].location = (240.48643493652344, -37.24143981933594)
    geometry_nodes_1.nodes["Join Geometry"].location = (943.202392578125, -48.090126037597656)
    geometry_nodes_1.nodes["Group Input.001"].location = (496.35443115234375, 137.89129638671875)
    geometry_nodes_1.nodes["Group Input.002"].location = (-63.10108947753906, -446.4671936035156)
    geometry_nodes_1.nodes["Group Input.003"].location = (-128.2467041015625, 425.9239807128906)
    geometry_nodes_1.nodes["Math"].location = (164.2056884765625, -288.0757751464844)

    # Set dimensions
    geometry_nodes_1.nodes["Group Input"].width  = 140.0
    geometry_nodes_1.nodes["Group Input"].height = 100.0

    geometry_nodes_1.nodes["Group Output"].width  = 140.0
    geometry_nodes_1.nodes["Group Output"].height = 100.0

    geometry_nodes_1.nodes["Instance on Points"].width  = 140.0
    geometry_nodes_1.nodes["Instance on Points"].height = 100.0

    geometry_nodes_1.nodes["Mesh Line"].width  = 140.0
    geometry_nodes_1.nodes["Mesh Line"].height = 100.0

    geometry_nodes_1.nodes["Bounding Box"].width  = 140.0
    geometry_nodes_1.nodes["Bounding Box"].height = 100.0

    geometry_nodes_1.nodes["Vector Math"].width  = 140.0
    geometry_nodes_1.nodes["Vector Math"].height = 100.0

    geometry_nodes_1.nodes["Separate XYZ"].width  = 140.0
    geometry_nodes_1.nodes["Separate XYZ"].height = 100.0

    geometry_nodes_1.nodes["Combine XYZ"].width  = 140.0
    geometry_nodes_1.nodes["Combine XYZ"].height = 100.0

    geometry_nodes_1.nodes["Vector Math.001"].width  = 140.0
    geometry_nodes_1.nodes["Vector Math.001"].height = 100.0

    geometry_nodes_1.nodes["Instance on Points.001"].width  = 140.0
    geometry_nodes_1.nodes["Instance on Points.001"].height = 100.0

    geometry_nodes_1.nodes["Mesh Line.001"].width  = 140.0
    geometry_nodes_1.nodes["Mesh Line.001"].height = 100.0

    geometry_nodes_1.nodes["Vector Math.002"].width  = 140.0
    geometry_nodes_1.nodes["Vector Math.002"].height = 100.0

    geometry_nodes_1.nodes["Join Geometry"].width  = 140.0
    geometry_nodes_1.nodes["Join Geometry"].height = 100.0

    geometry_nodes_1.nodes["Group Input.001"].width  = 140.0
    geometry_nodes_1.nodes["Group Input.001"].height = 100.0

    geometry_nodes_1.nodes["Group Input.002"].width  = 140.0
    geometry_nodes_1.nodes["Group Input.002"].height = 100.0

    geometry_nodes_1.nodes["Group Input.003"].width  = 140.0
    geometry_nodes_1.nodes["Group Input.003"].height = 100.0

    geometry_nodes_1.nodes["Math"].width  = 140.0
    geometry_nodes_1.nodes["Math"].height = 100.0


    # Initialize geometry_nodes_1 links

    # mesh_line.Mesh -> instance_on_points.Points
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Mesh Line"].outputs[0],
        geometry_nodes_1.nodes["Instance on Points"].inputs[0]
    )
    # group_input.Geometry -> bounding_box.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input"].outputs[0],
        geometry_nodes_1.nodes["Bounding Box"].inputs[0]
    )
    # bounding_box.Min -> vector_math.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Bounding Box"].outputs[1],
        geometry_nodes_1.nodes["Vector Math"].inputs[1]
    )
    # bounding_box.Max -> vector_math.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Bounding Box"].outputs[2],
        geometry_nodes_1.nodes["Vector Math"].inputs[0]
    )
    # vector_math.Vector -> separate_xyz.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Math"].outputs[0],
        geometry_nodes_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> combine_xyz.X
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Separate XYZ"].outputs[0],
        geometry_nodes_1.nodes["Combine XYZ"].inputs[0]
    )
    # vector_math_001.Vector -> mesh_line.Offset
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Math.001"].outputs[0],
        geometry_nodes_1.nodes["Mesh Line"].inputs[3]
    )
    # combine_xyz.Vector -> vector_math_001.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Combine XYZ"].outputs[0],
        geometry_nodes_1.nodes["Vector Math.001"].inputs[0]
    )
    # vector_math_002.Vector -> mesh_line_001.Offset
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Math.002"].outputs[0],
        geometry_nodes_1.nodes["Mesh Line.001"].inputs[3]
    )
    # vector_math_001.Vector -> vector_math_002.Vector
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Math.001"].outputs[0],
        geometry_nodes_1.nodes["Vector Math.002"].inputs[0]
    )
    # mesh_line_001.Mesh -> instance_on_points_001.Points
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Mesh Line.001"].outputs[0],
        geometry_nodes_1.nodes["Instance on Points.001"].inputs[0]
    )
    # join_geometry.Geometry -> group_output.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Join Geometry"].outputs[0],
        geometry_nodes_1.nodes["Group Output"].inputs[0]
    )
    # instance_on_points.Instances -> join_geometry.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Instance on Points"].outputs[0],
        geometry_nodes_1.nodes["Join Geometry"].inputs[0]
    )
    # vector_math_002.Vector -> mesh_line_001.Start Location
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Vector Math.002"].outputs[0],
        geometry_nodes_1.nodes["Mesh Line.001"].inputs[2]
    )
    # group_input_001.Geometry -> instance_on_points.Instance
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input.001"].outputs[0],
        geometry_nodes_1.nodes["Instance on Points"].inputs[2]
    )
    # group_input_002.Geometry -> instance_on_points_001.Instance
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input.002"].outputs[0],
        geometry_nodes_1.nodes["Instance on Points.001"].inputs[2]
    )
    # group_input_003.Pitch -> mesh_line.Count
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input.003"].outputs[1],
        geometry_nodes_1.nodes["Mesh Line"].inputs[0]
    )
    # math.Value -> mesh_line_001.Count
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Math"].outputs[0],
        geometry_nodes_1.nodes["Mesh Line.001"].inputs[0]
    )
    # group_input_002.Extra Lenses -> math.Value
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Group Input.002"].outputs[2],
        geometry_nodes_1.nodes["Math"].inputs[0]
    )
    # instance_on_points_001.Instances -> join_geometry.Geometry
    geometry_nodes_1.links.new(
        geometry_nodes_1.nodes["Instance on Points.001"].outputs[0],
        geometry_nodes_1.nodes["Join Geometry"].inputs[0]
    )

    return geometry_nodes_1
