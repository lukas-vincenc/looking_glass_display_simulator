import bpy
import math
import os
from concurrent.futures import ThreadPoolExecutor


def load_pixels(filepath):
    image = bpy.data.images.load(filepath)
    image.pixels[:]  # ensure it's loaded
    return list(image.pixels)  # flat RGBA float list


class DisplayImageRenderer(bpy.types.Operator):
    bl_idname = "qm.render_display_image"
    bl_label = "Render Display Image"
    bl_description = "Render a display-ready image from the generated cameras"

    shared_storage = None

    quilt_width = None
    quilt_height = None
    tile_width = None
    tile_height = None

    grid_cols = None
    grid_rows = None

    cam_count = None

    quilt = None

    def execute(self, context):
        scene = context.scene
        custom_props = scene.custom_props
        self.shared_storage = scene.shared_storage

        target_directory = custom_props.qm_quilt_render_target_directory

        if not target_directory:
            self.report({'ERROR'}, "Please select a target directory")
            return {'CANCELLED'}

        cameras = self.collect_sorted_cameras()
        if not cameras:
            self.report({'ERROR'}, "No quilt camera list found. Spawn cameras first.")
            return {'CANCELLED'}

        self.cam_count = len(cameras)
        self.grid_cols = math.ceil(math.sqrt(self.cam_count))
        self.grid_rows = math.ceil(self.cam_count / self.grid_cols)
        self.tile_width = scene.render.resolution_x
        self.tile_height = scene.render.resolution_y

        # prepare temp render directory
        temp_dir = os.path.join(target_directory, "quilt_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Render all cameras
        orig_camera = scene.camera
        orig_filepath = scene.render.filepath
        tile_paths = []

        for idx, cam in enumerate(cameras):
            scene.camera = cam
            out_path = os.path.join(temp_dir, f"tile_{idx:03d}.png")
            scene.render.filepath = out_path
            bpy.ops.render.render(write_still=True)
            tile_paths.append(out_path)

        scene.camera = orig_camera
        scene.render.filepath = orig_filepath

        # Create final output image
        self.quilt_width = self.tile_width * self.cam_count
        self.quilt_height = self.tile_height
        quilt_name = "Display_Image"

        if quilt_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[quilt_name])

        self.quilt = bpy.data.images.new(
            quilt_name, width=self.quilt_width, height=self.quilt_height
        )

        # --- build interleaved image ---
        self.build_interleaved_image(tile_paths)

        # Save output
        quilt_path = os.path.join(target_directory, "display_image.png")
        self.quilt.filepath_raw = quilt_path
        self.quilt.file_format = 'PNG'
        self.quilt.save()

        # cleanup temp tiles
        for path in tile_paths:
            try:
                os.remove(path)
            except OSError:
                pass

        return {'FINISHED'}

    # -------------------------------------------------------------------------
    # CAMERA COLLECTION
    # -------------------------------------------------------------------------

    def collect_sorted_cameras(self):
        objs = bpy.data.objects
        cameras = [
            objs.get(item.value)
            for item in self.shared_storage.camera_names
            if objs.get(item.value)
        ]
        cameras.sort(key=lambda cam: int(cam.name.split("_")[-1]))
        return cameras

    # -------------------------------------------------------------------------
    # INTERLEAVED ROW-BASED RENDERING
    # -------------------------------------------------------------------------

    def render_interleaved_row(self, out_y, tile_pixel_arrays):
        tile_w = self.tile_width
        tile_h = self.tile_height
        cam_count = self.cam_count
        quilt_w = self.quilt_width

        row_pixels = []

        # Repeat for every tile-row k (0 → tile_h-1)
        for k in range(tile_h):

            # For each tile i, append tile[i][k]
            for tile_index in range(cam_count):
                pix = tile_pixel_arrays[tile_index]

                src_start = (k * tile_w) * 4
                src_end = src_start + tile_w * 4

                row_pixels.extend(pix[src_start:src_end])

        # Write this huge chunk directly
        dst_start = out_y * quilt_w * 4
        dst_end = dst_start + quilt_w * 4
        self.quilt.pixels[dst_start:dst_end] = row_pixels

    def build_interleaved_image(self, tile_paths):
        """
        Build pixel-level interleaved quilt:
        Output pixel order per row:
        [ tile0[x], tile1[x], tile2[x], ... tileN[x] ] repeated for each x.
        """

        num_tiles = len(tile_paths)
        tile_w = self.tile_width
        tile_h = self.tile_height
        tile_px_count = tile_w * tile_h * 4  # RGBA

        max_workers = min(os.cpu_count(), 16)

        # Load tiles in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            tiles = list(ex.map(load_pixels, tile_paths))

        # PREPARE final buffer (very large)
        quilt_w = tile_w * num_tiles  # pixel-per-tile interleaving increases width
        quilt_h = tile_h
        total_px = quilt_w * quilt_h * 4

        quilt_buf = [0.0] * total_px

        # Worker for each output row
        def render_row(y):
            dst_start = y * quilt_w * 4
            write_index = dst_start

            # For each pixel x in the row
            for x in range(tile_w):

                # For each tile in order — place one pixel RGBA
                for t in range(num_tiles):
                    tile = tiles[t]

                    # Source index for tile pixel
                    src_index = (y * tile_w + x) * 4

                    # Copy RGBA

                    quilt_buf[write_index:write_index + 4] = tile[src_index:src_index + 4]
                    write_index += 4

        # Parallelize the rows
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            list(ex.map(render_row, range(quilt_h)))

        # Single assignment — Blender-friendly
        self.quilt.pixels = quilt_buf

    def load_tile_pixels(self, path):
        """Load one tile and return a flat float list of pixels."""
        img = bpy.data.images.load(path)
        # ensure loaded as list (not bpy_prop_array)
        return list(img.pixels[:])
