import math

import bpy
from bpy.props import (StringProperty, IntProperty, FloatProperty, PointerProperty)

from .cameras_spawner import CamerasSpawner
from .display_image_renderer import DisplayImageRenderer
from .quilt_renderer import QuiltRenderer


def update_camera_count(self, context):
    self.qm_camera_count = self.qm_x_views * self.qm_y_views


def update_cameras(self, context):
    from .cameras_spawner import sync_camera_array
    sync_camera_array(context)


# Custom properties shown in the extension UI panel
class CustomProps(bpy.types.PropertyGroup):
    qm_camera_count: IntProperty(
        name="Camera Count",
        default=48, min=1, max=200,
        update=update_cameras
    )
    qm_spacing: FloatProperty(
        name="Spacing",
        default=1.0, min=0.01, max=10.0,
        update=update_cameras
    )
    qm_focus_camera: PointerProperty(
        name="Source Camera",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'CAMERA',
        update=update_cameras
    )
    qm_quilt_render_target_directory: StringProperty(
        name="Directory",
        default="",
        description="Define the root path of the project",
        subtype='DIR_PATH'
    )
    qm_pitch: IntProperty(
        name="Pitch",
        default=355,
        min=1,
        max=1000
    )
    qm_tilt: FloatProperty(
        name="Tilt",
        default=0,
        min=-math.pi / 2,
        max=math.pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        precision=5
    )
    qm_center: FloatProperty(
        name="Center",
        default=0,
        min=-1,
        max=1,
    )
    qm_x_views: IntProperty(
        name="X",
        default=8,
        min=1,
        max=100,
        update=update_cameras
    )
    qm_y_views: IntProperty(
        name="Y",
        default=6,
        min=1,
        max=100,
        update=update_cameras
    )
    qm_view_x_resolution: IntProperty(
        name="X",
        default=960,
        min=1,
        max=10000
    )
    qm_view_y_resolution: IntProperty(
        name="Y",
        default=720,
        min=1,
        max=10000
    )


class QuiltMakerPanel(bpy.types.Panel):
    bl_label = "Quilt Maker"
    bl_idname = "QUILT_MAKER_PANEL_PT_qm"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuiltMaker'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.qm_custom_props

        layout.label(text="Spawn Camera Array:", icon="OUTLINER_COLLECTION")

        layout.label(text="Views Grid Dimensions:")
        layout.prop(cus_pt, "qm_x_views")
        layout.prop(cus_pt, "qm_y_views")

        cam_count = cus_pt.qm_x_views * cus_pt.qm_y_views
        layout.label(text=f"Camera Count: {cam_count}")

        layout.prop(cus_pt, "qm_focus_camera")
        layout.prop(cus_pt, "qm_spacing")

        layout.operator("qm.cameras_spawner")

        layout.separator()

        layout.label(text="Render Quilt:", icon="OUTLINER_COLLECTION")
        layout.prop(cus_pt, "qm_quilt_render_target_directory")
        layout.label(text="Resolution of One View:")
        layout.prop(cus_pt, "qm_view_x_resolution")
        layout.prop(cus_pt, "qm_view_y_resolution")
        layout.operator("qm.render_quilt")

        quilt_x = cus_pt.qm_x_views * cus_pt.qm_view_x_resolution
        quilt_y = cus_pt.qm_y_views * cus_pt.qm_view_y_resolution

        layout.label(text=f"Quilt Resolution: {quilt_x} x {quilt_y}")

        layout.separator()

        layout.label(text="Render Display Image:", icon="OUTLINER_COLLECTION")

        layout.prop(cus_pt, "qm_pitch")
        layout.prop(cus_pt, "qm_tilt")
        layout.prop(cus_pt, "qm_center")

        layout.operator("qm.render_display_image")


all_classes = [
    CustomProps,
    QuiltMakerPanel,
    CamerasSpawner,
    QuiltRenderer,
    DisplayImageRenderer
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.qm_custom_props = bpy.props.PointerProperty(type=CustomProps)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.qm_custom_props
