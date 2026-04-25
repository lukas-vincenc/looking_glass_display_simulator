import math
import bpy
import os
import numpy as np
from time import gmtime, strftime


class DisplayImageRenderer(bpy.types.Operator):
    bl_idname = "qm.render_display_image"
    bl_label = "Render Display Image"
    bl_description = "Render a hologram image"

    # Internal state for modal
    _timer = None
    _cameras = []
    _tile_paths = []
    _current_index = 0
    _temp_dir = ""
    _target_dir = ""

    def modal(self, context, event):
        # Allow user to cancel with ESC
        if event.type == 'ESC':
            self.cleanup_temp_files()
            context.workspace.status_text_set(None)
            self.report({'INFO'}, "Render Cancelled")
            return self.cancel(context)

        if event.type == 'TIMER':
            # Phase 1: Rendering Tiles
            if self._current_index < len(self._cameras):
                cam = self._cameras[self._current_index]
                self.render_single_tile(context.scene, cam, self._current_index)

                # Update progress in the status bar (bottom of Blender)
                progress = (self._current_index + 1) / len(self._cameras) * 100
                context.workspace.status_text_set(
                    f"Quilt Maker: Rendering View {self._current_index + 1}/{len(self._cameras)} ({int(progress)}%) - Press ESC to Cancel"
                )

                self._current_index += 1
                return {'RUNNING_MODAL'}

            # Phase 2: Processing and Cleanup
            else:
                context.workspace.status_text_set("Quilt Maker: Finalizing Image...")
                self.process_final_image(context)
                self.cleanup_temp_files()
                context.workspace.status_text_set(None)
                return self.cancel(context)

        return {'PASS_THROUGH'}

    def execute(self, context):
        scene = context.scene
        custom_props = scene.qm_custom_props
        self._target_dir = custom_props.qm_quilt_render_target_directory

        if not self._target_dir:
            self.report({'ERROR'}, "Please select a target directory")
            return {'CANCELLED'}

        # Find and sort cameras
        self._cameras = [obj for obj in bpy.data.objects if obj.name.startswith("QuiltCam")]
        self._cameras.sort(key=lambda cam: int(cam.name.split("_")[-1]))

        if not self._cameras:
            self.report({'ERROR'}, "No quilt cameras found. Spawn cameras first.")
            return {'CANCELLED'}

        # Setup temp directory
        self._temp_dir = os.path.join(self._target_dir, "quilt_temp")
        os.makedirs(self._temp_dir, exist_ok=True)

        self._tile_paths = []
        self._current_index = 0

        # Start Modal and Timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def render_single_tile(self, scene, cam, idx):
        scene.camera = cam
        out_path = os.path.join(self._temp_dir, f"tile_{idx:03d}.png")
        scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        self._tile_paths.append(out_path)

    def process_final_image(self, context):
        scene = context.scene
        custom_props = scene.qm_custom_props

        # 1. Load pixels from files
        tiles = []
        for p in self._tile_paths:
            img = bpy.data.images.load(p)
            tiles.append(list(img.pixels[:]))
            bpy.data.images.remove(img)  # Free memory immediately

        # 2. Build the image using NumPy
        final_pixels = self.build_display_image_logic(tiles, scene, custom_props)

        # 3. Create Blender Image
        out_name = "Display_Image"
        if out_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[out_name])

        out_img = bpy.data.images.new(
            out_name,
            width=scene.render.resolution_x,
            height=scene.render.resolution_y
        )

        # SPEED UP: Use foreach_set instead of .tolist()
        # This copies raw data directly to C-buffer, bypassing Python list creation overhead
        out_img.pixels.foreach_set(final_pixels.flatten())

        # 4. Save
        out_path = os.path.join(self._target_dir, self.build_file_name(custom_props))
        out_img.filepath_raw = out_path
        out_img.file_format = 'PNG'
        out_img.save()

        self.report({'INFO'}, f"Saved: {os.path.basename(out_path)}")

    def build_display_image_logic(self, tiles, scene, props):
        tile_w = scene.render.resolution_x
        tile_h = scene.render.resolution_y
        total_views = len(tiles)

        # Params
        tilt_factor = math.degrees(props.qm_tilt) / 100
        pitch = props.qm_pitch
        center = props.qm_center
        cs = 0.00013  # color_shift constant

        tiles_np = np.asarray(tiles, dtype=np.float32)

        y = np.arange(tile_h, dtype=np.float32)
        x = np.arange(tile_w, dtype=np.float32)
        sy = (y[:, None] / tile_h)
        sx = 1.0 - (x[None, :] / tile_w)

        view_pick = (sx + cs + sy * tilt_factor) * pitch - center
        view_pick = view_pick - np.floor(view_pick)
        view = (view_pick * (total_views - 1)).astype(np.int32)

        idx = (np.arange(tile_h)[:, None] * tile_w + np.arange(tile_w)[None, :]) * 4
        idx = idx.astype(np.int32)

        # Build output RGBA
        out = np.empty((tile_h, tile_w, 4), dtype=np.float32)
        out[..., 0] = tiles_np[view, idx]  # R
        out[..., 1] = tiles_np[view, idx + 1]  # G
        out[..., 2] = tiles_np[view, idx + 2]  # B
        out[..., 3] = 1.0  # A

        return out

    def cleanup_temp_files(self):
        for p in self._tile_paths:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except:
                    pass
        if os.path.exists(self._temp_dir) and not os.listdir(self._temp_dir):
            os.rmdir(self._temp_dir)

    def build_file_name(self, props):
        timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        tilt_deg = math.degrees(props.qm_tilt)
        return f"{timestamp}_P{props.qm_pitch}_T{tilt_deg:.2f}_C{props.qm_center}.png"

    def cancel(self, context):
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(DisplayImageRenderer)


def unregister():
    bpy.utils.unregister_class(DisplayImageRenderer)