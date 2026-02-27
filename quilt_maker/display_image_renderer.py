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
        out_buf = [0.0] * (out_w * out_h * 4)

        tilt_factor = self.tilt / 100
        pitch = self.pitch
        center = self.center
        cs = self.color_shift

        for y in range(out_h):
            sy = y / out_h
            row_offset = y * tile_w * 4

            for x in range(out_w):
                sx = 1 - (x / out_w)

                view_pick = (sx + cs + sy * tilt_factor) * pitch - center
                view_pick = view_pick - math.floor(view_pick)

                view = int(view_pick * (total_views - 1))

                src_i = row_offset + x * 4
                r = tiles[view][src_i]
                g = tiles[view][src_i + 1]
                b = tiles[view][src_i + 2]

                out_i = (y * out_w + x) * 4
                out_buf[out_i:out_i + 4] = (r, g, b, 1.0)

        return out_buf

    def build_display_image_numpy(self, tiles_list):
        # tiles_list is a list of flat pixel arrays
        tile_w, tile_h = self.tile_width, self.tile_height
        num_views = len(tiles_list)

        # 1. Convert tiles to a single 3D numpy array: (View, PixelIndex, RGBA)
        # This takes some memory, but is much faster for lookup
        all_views = np.array(tiles_list, dtype=np.float32)

        # 2. Create a grid of coordinates
        y_coords, x_coords = np.mgrid[0:tile_h, 0:tile_w]

        # Normalize coordinates
        sx = x_coords / tile_w
        sy = y_coords / tile_h

        # 3. Vectorized math (The view_pick formula)
        tilt_factor = self.tilt / 100
        view_indices = (sx + self.color_shift + sy * tilt_factor) * self.pitch - self.center
        view_indices = (view_indices - np.floor(view_indices)) * (num_views - 1)
        view_indices = view_indices.astype(np.int32)

        # 4. Advanced Indexing
        # We need to map (y, x) to the correct view and the correct pixel index
        pixel_indices = (y_coords * tile_w + x_coords)

        # This extracts the correct R, G, B, A for every pixel at once
        # Result shape: (tile_h, tile_w, 4)
        final_image = all_views[view_indices, pixel_indices]

        return final_image.flatten()

    def build_file_name(self):
        now = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        return now + '_pitch_' + str(self.pitch) + '_tilt_' + str(self.tilt) + '_center_' + str(self.center) + '.png'


def register():
    bpy.utils.register_class(DisplayImageRenderer)


def unregister():
    bpy.utils.unregister_class(DisplayImageRenderer)
