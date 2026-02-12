import bpy
import math
import os
from concurrent.futures import ThreadPoolExecutor
from time import gmtime, strftime


# ------------------------------------------------------------
# Helper: Load tile pixels
# ------------------------------------------------------------
def load_pixels(filepath):
    img = bpy.data.images.load(filepath)
    return list(img.pixels[:])  # flat RGBA floats


# ======================================================================
#   MAIN OPERATOR
# ======================================================================
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

        cameras = self.collect_sorted_cameras()
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

        # prepare temp render directory
        temp_dir = os.path.join(target_directory, "quilt_temp")
        os.makedirs(temp_dir, exist_ok=True)

        # render all cameras
        tile_paths = self.render_all_tiles(scene, cameras, temp_dir)

        # build quilt grid (NxM quilt texture)
        quilt_buf = self.build_grid_quilt(tile_paths)

        # Now run CPU shader to create final hologram display image:
        final_buf = self.build_display_image_from_quilt(
            quilt_buf,
            color_shift=0.00013  # 0.00013
        )

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

    # ==================================================================
    # CAMERA COLLECTION
    # ==================================================================
    def collect_sorted_cameras(self):
        objs = bpy.data.objects
        cams = [obj for obj in objs if obj.name.startswith("QuiltCamera")]
        cams.sort(key=lambda cam: int(cam.name.split("_")[-1]))
        return cams

    # ==================================================================
    # RENDER TILES
    # ==================================================================
    def render_all_tiles(self, scene, cameras, temp_dir):
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

    # ==================================================================
    # 1. BUILD THE QUILT GRID (NxM CAMERAS)
    # ==================================================================
    def build_grid_quilt(self, tile_paths):
        tile_w = self.tile_width
        tile_h = self.tile_height

        # load tiles in parallel
        with ThreadPoolExecutor(max_workers=min(os.cpu_count(), 16)) as ex:
            tiles = list(ex.map(load_pixels, tile_paths))

        quilt_w = self.grid_cols * tile_w
        quilt_h = self.grid_rows * tile_h

        total = quilt_w * quilt_h * 4
        quilt_buf = [0.0] * total

        # write each tile into its quilt block
        for idx, pix in enumerate(tiles):
            col = idx % self.grid_cols
            row = idx // self.grid_cols

            base_x = col * tile_w
            base_y = row * tile_h

            for y in range(tile_h):
                for x in range(tile_w):
                    src_i = (y * tile_w + x) * 4
                    dst_x = base_x + x
                    dst_y = base_y + y
                    dst_i = (dst_y * quilt_w + dst_x) * 4
                    quilt_buf[dst_i:dst_i+4] = pix[src_i:src_i+4]

        return quilt_buf

    # ==================================================================
    # 2. CPU VERSION OF THE HOLOGRAPHIC SHADER
    # ==================================================================
    def build_display_image_from_quilt(self, quilt_buf, color_shift):
        tile_w = self.tile_width
        tile_h = self.tile_height

        out_w = tile_w
        out_h = tile_h

        out_buf = [0.0] * (out_w * out_h * 4)

        quilt_w = self.grid_cols * tile_w

        # helper: read pixel from a tile (view index)
        def get_quilt_pixel(view, x, y):
            col = view % self.grid_cols
            row = view // self.grid_cols
            qx = col * tile_w + x
            qy = row * tile_h + y
            i = (qy * quilt_w + qx) * 4
            return quilt_buf[i:i+3]  # r g b

        total_views = self.grid_cols * self.grid_rows

        # Generate final image pixels
        for y in range(out_h):
            sy = y / out_h

            for x in range(out_w):
                sx = x / out_w

                view_pick = (sx + color_shift + sy * (self.tilt / 100)) * self.pitch - self.center
                view_pick = view_pick - math.floor(view_pick)

                # determine which tile to sample
                view = int(view_pick * (total_views - 1))

                # sample camera tile
                r, g, b = get_quilt_pixel(view, x, y)

                out_i = (y * out_w + x) * 4
                out_buf[out_i:out_i+4] = (r, g, b, 1.0)

        return out_buf

    def build_file_name(self):
        now = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        return now + '_pitch_' + str(self.pitch) + '_tilt_' + str(self.tilt) + '_center_' + str(self.center) + '.png'


def register():
    bpy.utils.register_class(DisplayImageRenderer)


def unregister():
    bpy.utils.unregister_class(DisplayImageRenderer)
