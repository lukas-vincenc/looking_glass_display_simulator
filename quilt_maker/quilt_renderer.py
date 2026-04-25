import bpy
import os
import numpy as np


class QuiltRenderer(bpy.types.Operator):
    bl_idname = "qm.render_quilt"
    bl_label = "Render Quilt"
    bl_description = "Render a quilt"

    _timer = None
    _cameras = []
    _tile_paths = []
    _current_index = 0
    _temp_dir = ""
    _target_dir = ""

    # Store original settings to restore later
    _orig_res_x = 0
    _orig_res_y = 0

    def modal(self, context, event):
        if event.type == 'ESC':
            self.cleanup(context)
            self.report({'INFO'}, "Quilt Render Cancelled")
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # Phase 1: Render Individual Tiles
            if self._current_index < len(self._cameras):
                progress = (self._current_index / len(self._cameras)) * 100
                context.workspace.status_text_set(
                    f"Quilt Maker: Rendering Tile {self._current_index + 1}/{len(self._cameras)} ({int(progress)}%) - ESC to Cancel"
                )

                # Force UI Refresh
                for area in context.screen.areas:
                    area.tag_redraw()

                cam = self._cameras[self._current_index]
                self.render_single_tile(context.scene, cam, self._current_index)

                self._current_index += 1
                return {'RUNNING_MODAL'}

            # Phase 2: Stitch Tiles into Quilt
            else:
                context.workspace.status_text_set("Quilt Maker: Stitching Quilt Grid...")
                self.process_quilt(context)
                self.cleanup(context)
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        scene = context.scene
        props = scene.qm_custom_props
        self._target_dir = bpy.path.abspath(props.qm_quilt_render_target_directory)

        if not self._target_dir or not os.path.exists(self._target_dir):
            self.report({'ERROR'}, "Invalid Target Directory")
            return {'CANCELLED'}

        self._cameras = [obj for obj in bpy.data.objects if obj.name.startswith("QuiltCam")]
        self._cameras.sort(key=lambda cam: int(cam.name.split("_")[-1]))

        if not self._cameras:
            self.report({'ERROR'}, "No quilt cameras found. Spawn array first.")
            return {'CANCELLED'}

        # Store and set resolution
        self._orig_res_x = scene.render.resolution_x
        self._orig_res_y = scene.render.resolution_y
        scene.render.resolution_x = props.qm_view_x_resolution
        scene.render.resolution_y = props.qm_view_y_resolution

        # Setup Temp Dir
        self._temp_dir = os.path.join(self._target_dir, "quilt_temp")
        os.makedirs(self._temp_dir, exist_ok=True)

        self._tile_paths = []
        self._current_index = 0

        # Start Modal
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def render_single_tile(self, scene, cam, idx):
        scene.camera = cam
        out_path = os.path.join(self._temp_dir, f"tile_{idx:03d}.png")
        scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        self._tile_paths.append(out_path)

    def process_quilt(self, context):
        props = context.scene.qm_custom_props
        cols = props.qm_x_views
        rows = props.qm_y_views
        tw = props.qm_view_x_resolution
        th = props.qm_view_y_resolution

        quilt_w = cols * tw
        quilt_h = rows * th

        # Pre-allocate the giant quilt array (RGBA)
        # We use uint8 for speed/memory if possible, or float32 for high bit depth
        quilt_data = np.zeros((quilt_h, quilt_w, 4), dtype=np.float32)

        for idx, path in enumerate(self._tile_paths):
            col = idx % cols
            # Calculate row from bottom-up (Blender image standard)
            row = idx // cols

            # Load tile
            img = bpy.data.images.load(path)
            tile_pixels = np.zeros(tw * th * 4, dtype=np.float32)
            img.pixels.foreach_get(tile_pixels)
            tile_pixels = tile_pixels.reshape((th, tw, 4))

            # Insert into quilt grid
            y_start = row * th
            y_end = y_start + th
            x_start = col * tw
            x_end = x_start + tw

            quilt_data[y_start:y_end, x_start:x_end] = tile_pixels

            bpy.data.images.remove(img)

        # Create and Save Result
        out_name = "Quilt_Result"
        if out_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[out_name])

        quilt_img = bpy.data.images.new(out_name, width=quilt_w, height=quilt_h)
        quilt_img.pixels.foreach_set(quilt_data.flatten())

        aspect_ratio = round(th / tw, 3)
        final_filename = f"{props.qm_filename}_qs{cols}x{rows}a{aspect_ratio}.png"
        save_path = os.path.join(self._target_dir, final_filename)
        quilt_img.filepath_raw = save_path
        quilt_img.file_format = 'PNG'
        quilt_img.save()

        self.report({'INFO'}, f"Quilt saved to: {save_path}")

    def cleanup(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)

        # Restore resolutions
        context.scene.render.resolution_x = self._orig_res_x
        context.scene.render.resolution_y = self._orig_res_y
        context.workspace.status_text_set(None)

        # Delete temp files
        for p in self._tile_paths:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except:
                    pass
        if os.path.exists(self._temp_dir):
            try:
                os.rmdir(self._temp_dir)
            except:
                pass

    def cancel(self, context):
        self.cleanup(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(QuiltRenderer)


def unregister():
    bpy.utils.unregister_class(QuiltRenderer)