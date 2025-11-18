import bpy
import math
import os
import threading

from concurrent.futures import ThreadPoolExecutor

# single-threaded: approximately 12 minutes (100x100)
# multi-threaded: approximately 15 seconds (100x100)

# multi-threaded: approximately 25 minutes (500x500)


def load_pixels(filepath):
    image = bpy.data.images.load(filepath)
    image.pixels[:]  # force loading
    return list(image.pixels)  # flat list of RGBA floats


class QuiltRenderer(bpy.types.Operator):
    bl_idname = "qm.render_quilt"
    bl_label = "Render Quilt"
    bl_description = "Render a quilt from the generated cameras"

    shared_storage = None

    quilt_width = None
    quilt_height = None
    tile_width = None
    tile_height = None

    grid_cols = None
    grid_rows = None

    quilt = None

    write_lock = threading.Lock()

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

        cam_count = len(cameras)
        self.grid_cols = math.ceil(math.sqrt(cam_count))
        self.grid_rows = math.ceil(cam_count / self.grid_cols)
        self.tile_width = scene.render.resolution_x
        self.tile_height = scene.render.resolution_y

        # prepare output directory
        temp_dir = os.path.join(target_directory, "quilt_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # render each camera
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

        # ---- create quilt image ----
        self.quilt_width = self.grid_cols * self.tile_width
        self.quilt_height = self.grid_rows * self.tile_height
        quilt_name = "Quilt_Image"

        # remove existing quilt image if present
        if quilt_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[quilt_name])

        self.quilt = bpy.data.images.new(quilt_name, width=self.quilt_width, height=self.quilt_height)

        # ---- copy pixels tile by tile ----
        max_workers = min(8, len(tile_paths))  # TODO: only temporary

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.render_tile, idx, path)
                for idx, path in enumerate(tile_paths)
            ]
            for f in futures:
                f.result()

        # ---- save quilt ----
        quilt_path = os.path.join(target_directory, "quilt.png")
        self.quilt.filepath_raw = quilt_path
        self.quilt.file_format = 'PNG'
        self.quilt.save()

        # cleanup
        scene.render.filepath = orig_filepath
        for path in tile_paths:
            try:
                os.remove(path)
            except OSError:
                pass

        return {'FINISHED'}

    def collect_sorted_cameras(self):
        objs = bpy.data.objects

        cameras = [
            objs.get(item.value)
            for item in self.shared_storage.camera_names
            if objs.get(item.value)
        ]

        # sort by the index at the end of the camera name
        cameras.sort(key=lambda cam: int(cam.name.split("_")[-1]))

        return cameras

    def render_tile(self, idx, path):
        pixels = load_pixels(path)

        col = idx % self.grid_cols
        row = idx // self.grid_cols

        tile_w = self.tile_width
        tile_h = self.tile_height

        quilt_w = self.quilt_width

        for y in range(tile_h):
            # source row slice
            src_start = y * tile_w * 4
            src_end = src_start + tile_w * 4

            row_data = pixels[src_start:src_end]

            # destination row index in quilt
            dst_y = row * tile_h + y
            dst_start = (dst_y * quilt_w + col * tile_w) * 4
            dst_end = dst_start + tile_w * 4

            # FAST: lock only around the shared pixel assignment
            with self.write_lock:
                self.quilt.pixels[dst_start:dst_end] = row_data
