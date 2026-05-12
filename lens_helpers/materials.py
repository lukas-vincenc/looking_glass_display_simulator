import bpy


def create_glass_material(mat_name, ior):
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # remove default nodes
    for node in nodes:
        nodes.remove(node)

    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    glass = nodes.new(type='ShaderNodeBsdfGlass')
    glass.location = (0, 0)

    glass.inputs['Roughness'].default_value = 0.0
    glass.inputs['IOR'].default_value = ior
    glass.inputs['Color'].default_value = (1, 1, 1, 1)

    links.new(glass.outputs['BSDF'], output.inputs['Surface'])

    return mat


def get_lens_material():
    mat_name = "LensMaterial"

    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]

    return create_glass_material(mat_name, 1.49)


def get_block_material(ior):
    mat_name = "BlockMaterial"

    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]

    return create_glass_material(mat_name, ior)
