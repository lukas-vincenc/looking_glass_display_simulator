import bpy
import math
import os


class QuiltRenderer(bpy.types.Operator):
    bl_idname = "qm.render_quilt"
    bl_label = "Render Quilt"
    bl_description = "Render a quilt from the generated cameras using compositor"

    tile_width = None
    tile_height = None

    grid_cols = None
    grid_rows = None

    def execute(self, context):
        scene = context.scene
        custom_props = scene.custom_props

        target_directory = custom_props.qm_quilt_render_target_directory

        if not target_directory:
            self.report({'ERROR'}, "Please select a target directory")
            return {'CANCELLED'}

        cameras = self.collect_sorted_cameras()
        if not cameras:
            self.report({'ERROR'}, "No quilt camera list found. Spawn cameras first.")
            return {'CANCELLED'}

        self.grid_cols = custom_props.qm_x_views
        self.grid_rows = custom_props.qm_y_views

        orig_res_x = scene.render.resolution_x
        orig_res_y = scene.render.resolution_y

        scene.render.resolution_x = custom_props.qm_view_x_resolution
        scene.render.resolution_y = custom_props.qm_view_y_resolution

        self.tile_width = custom_props.qm_view_x_resolution
        self.tile_height = custom_props.qm_view_y_resolution

        # -------------------------------------------------
        # Prepare temp directory
        # -------------------------------------------------
        temp_dir = os.path.join(target_directory, "quilt_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # -------------------------------------------------
        # Render tiles
        # -------------------------------------------------
        orig_camera = scene.camera
        orig_filepath = scene.render.filepath
        bpy.context.scene.use_nodes = False

        tile_paths = []

        for idx, cam in enumerate(cameras):
            scene.camera = cam
            out_path = os.path.join(temp_dir, f"tile_{idx:03d}.png")
            out_path = os.path.normpath(os.path.abspath(out_path))
            scene.render.filepath = out_path
            scene.render.image_settings.file_format = 'PNG'
            scene.render.image_settings.color_mode = 'RGBA'

            bpy.ops.render.render(write_still=True)
            bpy.context.view_layer.update()

            if not os.path.exists(out_path):
                raise RuntimeError(f"Render failed: {out_path}")

            tile_paths.append(out_path)

        scene.camera = orig_camera
        scene.render.filepath = orig_filepath

        # -------------------------------------------------
        # Build compositor quilt
        # -------------------------------------------------
        self.build_quilt_compositor(
            scene=scene,
            tile_paths=tile_paths,
            output_path=os.path.join(target_directory, "quilt.png")
        )

        # -------------------------------------------------
        # Cleanup temp tiles
        # -------------------------------------------------
        for p in tile_paths:
            try:
                os.remove(p)
            except:
                pass

        scene.render.resolution_x = orig_res_x
        scene.render.resolution_y = orig_res_y

        self.report({'INFO'}, "Quilt rendered successfully")
        return {'FINISHED'}

    # -------------------------------------------------
    # Camera collection
    # -------------------------------------------------
    def collect_sorted_cameras(self):
        objs = bpy.data.objects
        cams = [obj for obj in objs if obj.name.startswith("QuiltCamera")]
        cams.sort(key=lambda cam: int(cam.name.split("_")[-1]))
        return cams

    # -------------------------------------------------
    # Compositor builder
    # -------------------------------------------------
    def build_quilt_compositor(self, scene, tile_paths, output_path):
        scene.use_nodes = True
        nt = scene.node_tree
        nt.nodes.clear()

        quilt_w = self.grid_cols * self.tile_width
        quilt_h = self.grid_rows * self.tile_height

        orig_resolution_x = scene.render.resolution_x
        orig_resolution_y = scene.render.resolution_y

        # resize render canvas
        scene.render.resolution_x = quilt_w
        scene.render.resolution_y = quilt_h
        scene.render.resolution_percentage = 100

        comp_node = nt.nodes.new("CompositorNodeComposite")
        comp_node.location = (1200, 0)

        # -------------------------------------------------
        # FULL-SIZE TRANSPARENT CANVAS
        # -------------------------------------------------
        bg_img = bpy.data.images.new(
            name="Quilt_BG",
            width=quilt_w,
            height=quilt_h,
            alpha=True
        )

        bg_node = nt.nodes.new("CompositorNodeImage")
        bg_node.image = bg_img
        bg_node.location = (-300, 0)
        alpha_chain = bg_node

        for i, path in enumerate(tile_paths):
            col = i % self.grid_cols
            row = i // self.grid_cols

            img_node = nt.nodes.new("CompositorNodeImage")
            img_node.image = bpy.data.images.load(path)
            img_node.location = (0, -300 * i)

            inv_col = (self.grid_cols - 1) - col
            inv_row = (self.grid_rows - 1) - row

            trans_node = nt.nodes.new("CompositorNodeTransform")
            trans_node.inputs['X'].default_value = ((self.grid_cols - 1) / 2 - inv_col) * self.tile_width
            trans_node.inputs['Y'].default_value = ((self.grid_rows - 1) / 2 - inv_row) * self.tile_height
            trans_node.inputs['Scale'].default_value = 1.0
            trans_node.location = (300, -300 * i)

            nt.links.new(img_node.outputs['Image'], trans_node.inputs['Image'])

            mix = nt.nodes.new("CompositorNodeAlphaOver")
            mix.location = (600, -300 * i)

            # background → input 1
            nt.links.new(alpha_chain.outputs[0], mix.inputs[1])
            # tile → input 2
            nt.links.new(trans_node.outputs['Image'], mix.inputs[2])

            alpha_chain = mix

        nt.links.new(alpha_chain.outputs['Image'], comp_node.inputs['Image'])

        scene.render.filepath = os.path.normpath(os.path.abspath(output_path))
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'

        bpy.ops.render.render(write_still=True)

        scene.render.resolution_x = orig_resolution_x
        scene.render.resolution_y = orig_resolution_y
