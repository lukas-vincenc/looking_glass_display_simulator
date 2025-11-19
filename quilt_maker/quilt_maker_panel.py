import bpy
from bpy.props import (StringProperty, IntProperty, FloatProperty, PointerProperty)

from .cameras_spawner import CamerasSpawner
from .display_image_renderer import DisplayImageRenderer
from .quilt_renderer import QuiltRenderer


# Custom properties shown in the extension UI panel
class CustomProps(bpy.types.PropertyGroup):
    qm_camera_count: IntProperty(
        name="Camera Count",
        default=45,
        min=1,
        max=200
    )
    qm_focus_distance: FloatProperty(
        name="Focus Distance",
        default=30.0,
        min=0.1,
        max=1000.0
    )
    qm_focus_object: PointerProperty(
        name="Focus",
        type=bpy.types.Object
    )
    qm_quilt_render_target_directory: StringProperty(
        name="Directory",
        default="",
        description="Define the root path of the project",
        subtype='DIR_PATH'
    )


class StringValueItem(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


# get rid of the shared storage, only introduces bugs
class SharedStorage(bpy.types.PropertyGroup):
    camera_names: bpy.props.CollectionProperty(type=StringValueItem)


class QuiltMakerPanel(bpy.types.Panel):
    bl_label = "Quilt Maker"
    bl_idname = "QUILT_MAKER_PANEL_PT_qm"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuiltMaker'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.custom_props

        layout.label(text="Spawn Camera Array:")

        layout.prop(cus_pt, "qm_camera_count")
        layout.prop(cus_pt, "qm_focus_distance")
        layout.prop(cus_pt, "qm_focus_object")

        layout.operator("qm.cameras_spawner")

        layout.separator()

        layout.label(text="Render Quilt:")
        layout.prop(cus_pt, "qm_quilt_render_target_directory")
        layout.operator("qm.render_quilt")

        layout.separator()

        layout.label(text="Render Display Image:")
        layout.operator("qm.render_display_image")


all_classes = [
    CustomProps,
    StringValueItem,
    SharedStorage,
    QuiltMakerPanel,
    CamerasSpawner,
    QuiltRenderer,
    DisplayImageRenderer
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)

    # TODO: change to qm_custom_props
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProps)
    bpy.types.Scene.shared_storage = bpy.props.PointerProperty(type=SharedStorage)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.custom_props
    del bpy.types.Scene.shared_storage
