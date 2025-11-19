from .display_simulator import display_simulator_panel
from .quilt_maker import quilt_maker_panel

bl_info = {
    "name": "Lenticular Display Simulator",
    "author": "Lukas Vincenc",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Lenticular Display Simulator",
    "description": "Simulate a lenticular display",
    "category": "3D View",
}


def register():
    quilt_maker_panel.register()
    display_simulator_panel.register()


def unregister():
    quilt_maker_panel.unregister()
    display_simulator_panel.unregister()


if __name__ == "__main__":
    register()
