import bpy
import math
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from time import gmtime, strftime


def load_pixels(filepath):
    img = bpy.data.images.load(filepath)
    return list(img.pixels[:])  # flat RGBA floats


def load_tiles(tile_paths):
    with ThreadPoolExecutor(max_workers=min(os.cpu_count(), 16)) as ex:
        return list(ex.map(load_pixels, tile_paths))


def render_all_tiles(scene, cameras, temp_dir):
    orig_cam = scene.camera
    orig_path = scene.render.filepath

    tile_paths = []

    for idx, cam in enumerate(cameras):
        scene.camera = cam
        out_path = os.path.join(temp_dir, f"tile_{idx:03d}.png")
        scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        tile_paths.append(out_path)

    scene.camera = orig_cam
    scene.render.filepath = orig_path

    return tile_paths


def collect_sorted_cameras():
    objs = bpy.data.objects
    cams = [obj for obj in objs if obj.name.startswith("QuiltCamera")]
    cams.sort(key=lambda cam: int(cam.name.split("_")[-1]))
    return cams


class DisplayImageRenderer(bpy.types.Operator):
    bl_idname = "qm.render_display_image"
    bl_label = "Render Display Image"
    bl_description = "Render a display-ready hologram image from quilt cameras"

    quilt_width = None
    quilt_height = None
    tile_width = None
    tile_height = None

    grid_cols = None
    grid_rows = None

    cam_count = None
    quilt = None

    pitch = None  # 354.677
    tilt = None  # -0.113949
    center = 0  # -0.400272
    color_shift = 0.00013  # 0.00013

    # ------------------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------------------
    def execute(self, context):
        scene = context.scene
        custom_props = scene.custom_props

        target_directory = custom_props.qm_quilt_render_target_directory

        if not target_directory:
            self.report({'ERROR'}, "Please select a target directory")
            return {'CANCELLED'}

        cameras = collect_sorted_cameras()
        if not cameras:
            self.report({'ERROR'}, "No quilt camera list found. Spawn cameras first.")
            return {'CANCELLED'}

        self.cam_count = len(cameras)
        self.grid_cols = math.ceil(math.sqrt(self.cam_count))
        self.grid_rows = math.ceil(self.cam_count / self.grid_cols)
        self.tile_width = scene.render.resolution_x
        self.tile_height = scene.render.resolution_y

        self.pitch = custom_props.qm_pitch
        self.tilt = math.degrees(custom_props.qm_tilt)

        bpy.context.scene.use_nodes = False

        # prepare temp render directory
        temp_dir = os.path.join(target_directory, "quilt_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # render all cameras
        tile_paths = render_all_tiles(scene, cameras, temp_dir)

        tiles = load_tiles(tile_paths)
        final_buf = self.build_display_image_from_tiles(tiles)

        # create final image in Blender
        out_name = "Display_Image"
        if out_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[out_name])

        out_img = bpy.data.images.new(
            out_name,
            width=self.tile_width,
            height=self.tile_height
        )
        out_img.pixels = final_buf

        # save
        out_path = os.path.join(target_directory, self.build_file_name())
        out_img.filepath_raw = out_path
        out_img.file_format = 'PNG'
        out_img.save()

        # cleanup
        for p in tile_paths:
            try:
                os.remove(p)
            except:
                pass

        return {'FINISHED'}

    def build_display_image_from_tiles(self, tiles):
        tile_w = self.tile_width
        tile_h = self.tile_height
        out_w = tile_w
        out_h = tile_h

        total_views = len(tiles)

        tilt_factor = self.tilt / 100
        pitch = self.pitch
        center = self.center
        cs = self.color_shift

        # Convert tiles to numpy: shape = (views, H*W*4)
        tiles_np = np.asarray(tiles, dtype=np.float32)

        # Create coordinate grids
        y = np.arange(out_h, dtype=np.float32)
        x = np.arange(out_w, dtype=np.float32)

        sy = (y[:, None] / out_h)
        sx = 1.0 - (x[None, :] / out_w)

        # Compute view_pick
        view_pick = (sx + cs + sy * tilt_factor) * pitch - center
        view_pick = view_pick - np.floor(view_pick)

        # View index
        view = (view_pick * (total_views - 1)).astype(np.int32)  # shape (H,W)

        # Pixel indices inside flat tile buffer
        idx = (np.arange(out_h)[:, None] * tile_w + np.arange(out_w)[None, :]) * 4
        idx = idx.astype(np.int32)  # shape (H,W)

        # Gather RGB

        r = tiles_np[view, idx]
        g = tiles_np[view, idx + 1]
        b = tiles_np[view, idx + 2]

        # Build output buffer
        out = np.empty((out_h, out_w, 4), dtype=np.float32)
        out[..., 0] = r
        out[..., 1] = g
        out[..., 2] = b
        out[..., 3] = 1.0  # alpha

        # Return flat buffer like original
        return out.reshape(-1).tolist()

    def build_file_name(self):
        now = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        return now + '_pitch_' + str(self.pitch) + '_tilt_' + str(self.tilt) + '_center_' + str(self.center) + '.png'


def register():
    bpy.utils.register_class(DisplayImageRenderer)


def unregister():
    bpy.utils.unregister_class(DisplayImageRenderer)
