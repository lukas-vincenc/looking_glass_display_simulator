import math
import bpy
import os


class InterlacedImageExporter(bpy.types.Operator):
    bl_idname = "export.shader_result"
    bl_label = "Export Interlaced Image"
    bl_description = "Export the quilt transformed into the display-ready image"

    def execute(self, context):
        scene = context.scene
        props = scene.lds_custom_props

        target_dir = bpy.path.abspath(props.lds_output_dir)
        filename = props.lds_output_filename

        if not target_dir or not os.path.exists(target_dir):
            self.report({'ERROR'}, "Invalid Target Directory")
            return {'CANCELLED'}

        if not filename:
            self.report({'ERROR'}, "Invalid Filename")
            return {'CANCELLED'}

        # Get material
        mat = bpy.data.materials.get("Display_Image_Interlacer")
        if not mat or not mat.node_tree:
            self.report({'ERROR'}, "Material not found or has no nodes")
            return {'CANCELLED'}

        obj = bpy.data.objects.get("ImagePlane")
        if not obj:
            self.report({'ERROR'}, "ImagePlane not found")
            return {'CANCELLED'}

        # Cycles required for baking
        bpy.context.scene.render.engine = 'CYCLES'

        x_res = props.lds_x_resolution
        y_res = round(x_res * props.lds_height / props.lds_width)

        # Create image
        img = bpy.data.images.new("BakedImage", width=x_res, height=y_res)

        # Add image texture node
        nodes = mat.node_tree.nodes
        img_node = nodes.new("ShaderNodeTexImage")
        img_node.image = img
        nodes.active = img_node

        # Make sure object is selected & active
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Bake emission
        bpy.ops.object.bake(type='EMIT')

        # Save image
        target_dir = bpy.path.abspath(props.lds_output_dir)
        save_path = os.path.join(target_dir, f"{props.lds_output_filename}.png")
        img.filepath_raw = save_path
        img.file_format = 'PNG'
        img.save()

        # Cleanup
        nodes.remove(img_node)

        self.report({'INFO'}, "Image exported successfully")
        return {'FINISHED'}
