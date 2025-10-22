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


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
