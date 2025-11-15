import bpy
from bpy.props import (IntProperty, FloatProperty, PointerProperty)

from .cameras_spawner import CamerasSpawner


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
        name="Focus Object",
        type=bpy.types.Object
    )


class QuiltMakerPanel(bpy.types.Panel):
    bl_label = "Quilt Maker"
    bl_idname = "QUILT_MAKER_PANEL_PT_suffix"  # TODO: suffix?
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

        layout.separator()
        layout.operator("qm.cameras_spawner")


all_classes = [
    CustomProps,
    QuiltMakerPanel,
    CamerasSpawner
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProps)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.custom_props
