import bpy
from bpy.props import IntProperty

from .display_spawner import DisplaySpawner


# Custom properties shown in the extension UI panel
class CustomProps(bpy.types.PropertyGroup):
    lds_width: IntProperty(
        name="Width (px)",
        default=1920,
        min=1,
        max=2000
    )
    lds_height: IntProperty(
        name="Height (px)",
        default=1080,
        min=1,
        max=2000
    )


class DisplaySimulatorPanel(bpy.types.Panel):
    bl_label = "Lenticular Display Simulator"
    bl_idname = "LENTICULAR DISPLAY SIMULATOR_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LentDisplay'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.lds_custom_props

        layout.prop(cus_pt, "lds_width")
        layout.prop(cus_pt, "lds_height")

        layout.operator("object.display_spawner", text="Spawn Display")


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
