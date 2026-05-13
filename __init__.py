# -----------------------------------------------------------------
# ---------------- Looking Glass Display Simulator ----------------
# ------------------- Lukas Vincenc - xvince01 --------------------
# -----------------------------------------------------------------

from .display_simulator import display_simulator_panel
from .quilt_maker import quilt_maker_panel
from .lens_visualization import lens_visualization_panel

bl_info = {
    "name": "Looking Glass Display Simulator",
    "author": "Lukas Vincenc",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Looking Glass Display Simulator",
    "description": "Simulate a Looking Glass display",
    "category": "3D View",
}


def register():
    quilt_maker_panel.register()
    display_simulator_panel.register()
    lens_visualization_panel.register()


def unregister():
    quilt_maker_panel.unregister()
    display_simulator_panel.unregister()
    lens_visualization_panel.unregister()


if __name__ == "__main__":
    register()
