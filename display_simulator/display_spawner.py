import bpy


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


class DisplaySpawner(bpy.types.Operator):
    bl_idname = "object.display_spawner"
    bl_label = "Display Spawner"
    bl_description = "Spawns lenses creating the display"

    def execute(self, context):
        scene = context.scene
        custom_props = scene.lds_custom_props

        lens_count = custom_props.lds_width
        lens_radius = 0.005
        lens_height = custom_props.lds_height * lens_radius * 2
        spacing = lens_radius * 2.0
        flatten_offset = lens_radius * 0.5
        cylinder_vertices = 128

        # clear old lenses
        for obj in bpy.data.objects:
            if obj.name.startswith("Lens_") or obj.name.startswith("Flatten_"):
                bpy.data.objects.remove(obj, do_unlink=True)

        material = get_lens_material()

        for i in range(lens_count):
            # creates a cylinder
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=cylinder_vertices,
                radius=lens_radius,
                depth=lens_height,
                location=(i * spacing, 0, 0)
            )
            cyl = bpy.context.object
            cyl.name = f"Lens_{i:03d}"

            # creates a matching cube to flatten the cylinder
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(i * spacing, flatten_offset, 0)
            )
            cube = bpy.context.object
            cube.name = f"Flatten_{i:03d}"

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

        return {'FINISHED'}
