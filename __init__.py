import bpy

from .operators.cameras_spawner import CamerasSpawner
from .operators.display_spawner import DisplaySpawner
from .panels.main_panel import MainPanel
from .panels.quilt_maker_panel import QuiltMakerPanel

bl_info = {
    "name": "Lenticular Display Simulator",
    "author": "Lukas Vincenc",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Lenticular Display Simulator",
    "description": "Simulate a lenticular display",
    "category": "3D View",
}


classes = (
    DisplaySpawner,
    CamerasSpawner,
    MainPanel,
    QuiltMakerPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.qm_camera_count = bpy.props.IntProperty(
        name="Camera Count",
        default=45,
        min=1,
        max=200
    )
    bpy.types.Scene.qm_focus_distance = bpy.props.FloatProperty(
        name="Focus Distance",
        default=30.0,
        min=0.1,
        max=1000.0
    )
    bpy.types.Scene.qm_focus_object = bpy.props.PointerProperty(
        name="Focus Object",
        type=bpy.types.Object
    )


def unregister():
    del bpy.types.Scene.qm_camera_count
    del bpy.types.Scene.qm_focus_distance
    del bpy.types.Scene.qm_focus_object

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
