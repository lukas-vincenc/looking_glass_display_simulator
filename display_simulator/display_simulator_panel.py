import math
import os
import re

import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty

from ..lens_helpers.lens_builder import set_lens_location_rotation_and_scale, resize_lens_to_correct_size
from .image_plane_spawner import spawn_image_plane, transform_quilt_and_spawn, update_display_image_params
from .lens_geometry_nodes import update_gn_pitch
from ..lens_helpers.lens_math import calculate_lens_parameters
from .display_spawner import DisplaySpawner


def update_geometry_nodes(obj, params, pitch):
    gn_mod = obj.modifiers.get("LDS_GeometryNodes")
    if not gn_mod or not gn_mod.node_group:
        return

    update_gn_pitch(gn_mod, pitch, params.missing_lenses)


def recalc_lens_geometry(self, context):
    obj = bpy.data.objects.get("Lens")
    if obj is None or "_base_mesh" not in obj or "_base_size" not in obj:
        return

    custom_props = context.scene.lds_custom_props
    display_width = DisplaySpawner.DISPLAY_WIDTH

    params = calculate_lens_parameters(
        display_width=display_width,
        pitch=custom_props.lds_pitch,
        height=custom_props.lds_height,
        width=custom_props.lds_width,
        width_percentage=custom_props.lds_lens_width,
        depth=custom_props.lds_depth,
        tilt=custom_props.lds_tilt,
        center=custom_props.lds_center,
    )

    update_geometry_nodes(obj, params, custom_props.lds_pitch)

    # Reset mesh
    obj.data = obj["_base_mesh"].copy()

    set_lens_location_rotation_and_scale(obj, params, display_width)
    resize_lens_to_correct_size(obj, params, obj["_base_size"])


# TODO: possible delete
# def update_display_image(self, context):
#     path = self.lds_image_path
#     if not path:
#         return
#
#     try:
#         img = bpy.data.images.load(path, check_existing=True)
#     except:
#         print("Invalid image path")
#         return
#
#     # Remove old plane if exists
#     if "ImagePlane" in bpy.data.objects:
#         old = bpy.data.objects["ImagePlane"]
#         bpy.data.objects.remove(old, do_unlink=True)
#
#     spawn_image_plane(img, context)


def parse_quilt_settings(filepath):
    filename = os.path.basename(filepath)
    pattern = r"qs(\d+)x(\d+)a(\d*\.?\d+)"
    match = re.search(pattern, filename)

    if match:
        return {
            'x': int(match.group(1)),
            'y': int(match.group(2)),
            'ratio': float(match.group(3))
        }
    return None


def update_quilt_image(self, context):
    path = self.lds_quilt_path
    if not path:
        return

    custom_props = context.scene.lds_custom_props

    try:
        img = bpy.data.images.load(path, check_existing=True)
    except:
        print("Invalid image path")
        return

    params = parse_quilt_settings(path)

    if params is not None:
        custom_props.lds_x_tiles = params["x"]
        custom_props.lds_y_tiles = params["y"]
        custom_props.lds_width = 1
        custom_props.lds_height = params["ratio"]

        lens = bpy.data.objects.get("Lens")
        block = bpy.data.objects.get("RefractiveBlock")
        if lens is None and block is None:
            try:
                bpy.ops.object.display_spawner()
            except Exception as e:
                print(f"Could not trigger display spawner: {e}")

    # Remove old plane if exists
    if "ImagePlane" in bpy.data.objects:
        old = bpy.data.objects["ImagePlane"]
        bpy.data.objects.remove(old, do_unlink=True)

    transform_quilt_and_spawn(
        img,
        context,
        custom_props.lds_image_pitch,
        custom_props.lds_image_tilt,
        custom_props.lds_image_center,
        custom_props.lds_width,
        custom_props.lds_height,
        custom_props.lds_x_tiles,
        custom_props.lds_y_tiles
    )


def update_block(self, context):
    obj = bpy.data.objects.get("RefractiveBlock")
    if obj is None:
        return

    obj.scale.y = self.lds_block_depth


def update_display_image_param(self, context):
    custom_props = context.scene.lds_custom_props

    update_display_image_params(
        custom_props.lds_image_pitch,
        custom_props.lds_image_tilt,
        custom_props.lds_image_center,
        custom_props.lds_width,
        custom_props.lds_height,
        custom_props.lds_x_tiles,
        custom_props.lds_y_tiles
    )


def update_plane_height(height):
    plane = bpy.data.objects.get("ImagePlane")
    if plane is None:
        return

    plane.scale.y = height
    plane.location.z = height / 2


def update_block_height(height):
    block = bpy.data.objects.get("RefractiveBlock")
    if block is None:
        return

    block.scale.z = height


def update_aspect_ratio(self, context):
    custom_props = context.scene.lds_custom_props

    height = custom_props.lds_height / (custom_props.lds_width * DisplaySpawner.DISPLAY_WIDTH)

    update_plane_height(height)
    update_block_height(height)

    update_display_image_param(self, context)
    recalc_lens_geometry(self, context)


# Custom properties shown in the extension UI panel
class CustomProps(bpy.types.PropertyGroup):
    # lds_image_path: StringProperty(
    #     name="Display Image",
    #     description="Select a ready display image to spawn as plane",
    #     subtype='FILE_PATH',
    #     update=update_display_image
    # )

    # Quilt Setting
    lds_quilt_path: StringProperty(
        name="Quilt",
        description="Select a quilt image to transform and spawn as plane\n\n"
                    "File naming convention: filename_qs8x6a0.75 where\n"
                    "8 = x tiles\n"
                    "6 = y tiles\n"
                    "0.75 = aspect ratio (4:3)",
        subtype='FILE_PATH',
        update=update_quilt_image
    )
    lds_x_tiles: IntProperty(
        name="X tiles",
        default=8,
        min=1,
        max=100,
        update=update_display_image_param
    )
    lds_y_tiles: IntProperty(
        name="Y tiles",
        default=6,
        min=1,
        max=100,
        update=update_display_image_param
    )
    # Aspect Ratio
    lds_width: FloatProperty(
        name="Width",
        default=16,
        min=0.1,
        max=1000,
        precision=2,
        update=update_aspect_ratio
    )
    lds_height: FloatProperty(
        name="Height",
        default=9,
        min=0.1,
        max=1000,
        precision=2,
        update=update_aspect_ratio
    )
    # Display Image Settings
    lds_image_pitch: IntProperty(
        name="Pitch",
        default=355,
        min=1,
        max=1000,
        update=update_display_image_param
    )
    lds_image_tilt: FloatProperty(
        name="Tilt",
        default=math.radians(11),
        min=-math.pi / 2,
        max=math.pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        precision=5,
        update=update_display_image_param
    )
    lds_image_center: FloatProperty(
        name="Center",
        default=0,
        min=-1,
        max=1,
        update=update_display_image_param
    )
    # Display Settings
    lds_pitch: IntProperty(
        name="Pitch",
        default=355,
        min=1,
        max=1000,
        update=recalc_lens_geometry
    )
    lds_tilt: FloatProperty(
        name="Tilt",
        default=math.radians(10.85),
        min=-math.pi / 2,
        max=math.pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        precision=5,
        update=recalc_lens_geometry
    )
    lds_center: FloatProperty(
        name="Center",
        default=0,
        min=-1,
        max=1,
        update=recalc_lens_geometry
    )
    lds_block_depth: FloatProperty(
        name="Block Depth",
        default=0.25,
        subtype='DISTANCE',
        update=update_block
    )
    # Static Lens Config
    lds_depth: FloatProperty(
        name="Lens Depth",
        default=3,
        unit='NONE'
    )
    lds_lens_width: FloatProperty(
        name="Lens Width",
        default=200 / 3,
        min=0,
        max=100,
        subtype='PERCENTAGE'
    )


class DisplaySimulatorPanel(bpy.types.Panel):
    bl_label = "Lenticular Display Simulator"
    bl_idname = "LENTICULAR_DISPLAY_SIMULATOR_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LentDisplay'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.lds_custom_props

        layout.label(text="Input Quilt", icon="OUTLINER_COLLECTION")

        # layout.prop(cus_pt, "lds_image_path")
        layout.prop(cus_pt, "lds_quilt_path")

        layout.prop(cus_pt, "lds_x_tiles")
        layout.prop(cus_pt, "lds_y_tiles")

        layout.separator()

        layout.label(text="Display Aspect Ratio", icon="OUTLINER_COLLECTION")

        layout.prop(cus_pt, "lds_width")
        layout.prop(cus_pt, "lds_height")

        layout.separator()

        layout.label(text="Display Image Settings", icon="OUTLINER_COLLECTION")

        layout.prop(cus_pt, "lds_image_pitch")
        layout.prop(cus_pt, "lds_image_tilt")
        layout.prop(cus_pt, "lds_image_center")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Dynamic lens configuration", icon="OUTLINER_COLLECTION")
        row = col.row()
        row.enabled = False
        row.label(text="(changes in real-time)")

        layout.prop(cus_pt, "lds_pitch")
        layout.prop(cus_pt, "lds_tilt")
        layout.prop(cus_pt, "lds_center")

        layout.prop(cus_pt, "lds_block_depth")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Static lens configuration", icon="OUTLINER_COLLECTION")
        row = col.row()
        row.enabled = False
        row.label(text="(needs scene reloading to take effect)")

        layout.prop(cus_pt, "lds_depth")
        layout.prop(cus_pt, "lds_lens_width")

        layout.separator()

        layout.operator("object.display_spawner", text="Load Display")


all_classes = [
    CustomProps,
    DisplaySimulatorPanel,
    DisplaySpawner
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lds_custom_props = bpy.props.PointerProperty(type=CustomProps)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lds_custom_props
