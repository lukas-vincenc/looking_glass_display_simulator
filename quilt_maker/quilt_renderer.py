import bpy
import math
import os
import threading


def load_pixels(filepath):
    image = bpy.data.images.load(filepath)
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
            try:
                bpy.data.images.remove(bpy.data.images[quilt_name])
            except Exception:
                pass

        self.quilt = bpy.data.images.new(quilt_name, width=self.quilt_width, height=self.quilt_height)

        self.build_grid_image(tile_paths)

        # ---- save quilt ----
        quilt_path = os.path.join(target_directory, "quilt.png")
        self.quilt.filepath_raw = quilt_path
        self.quilt.file_format = 'PNG'
        self.quilt.save()

        # cleanup
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

    def build_grid_image(self, tile_paths):
        num_tiles = len(tile_paths)
        tile_w = self.tile_width
        tile_h = self.tile_height

        quilt_w = self.quilt_width
        quilt_h = self.quilt_height

        # load each tile image into a plain list of floats
        tiles = []
        for p in tile_paths:
            tiles.append(load_pixels(p))

        # allocate a buffer for the final quilt image (floats 0..1)
        total_px = quilt_w * quilt_h * 4
        quilt_buf = [0.0] * total_px

        for t_index in range(num_tiles):
            col = t_index % self.grid_cols
            row = t_index // self.grid_cols
            tile_pixels = tiles[t_index]  # flat list length tile_w*tile_h*4

            # For each pixel in the tile, copy into the quilt buffer at proper offset.
            for ty in range(tile_h):
                src_row_start = (ty * tile_w) * 4
                dest_y = row * tile_h + ty
                dest_row_start = (dest_y * quilt_w) * 4

                dest_x_offset = col * tile_w * 4

                # copy a whole row of pixels
                # each pixel is 4 floats
                src_idx = src_row_start
                dst_idx = dest_row_start + dest_x_offset
                quilt_buf[dst_idx: dst_idx + tile_w * 4] = tile_pixels[src_idx: src_idx + tile_w * 4]

        self.quilt.pixels = quilt_buf
