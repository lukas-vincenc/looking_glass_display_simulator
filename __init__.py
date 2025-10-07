bl_info = {
    "name": "Lenticular Display Simulator",
    "author": "Lukas Vincenc",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > My Addon",
    "description": "Simulate a lenticular display",
    "category": "3D View",
}

import bpy
from .operators.my_operator import MY_OT_sample_operator
from .panels.my_panel import MY_PT_sample_panel

classes = (
    MY_OT_sample_operator,
    MY_PT_sample_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
