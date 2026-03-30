import bpy

from .lens_math import LensParameters

all_classes = [
    LensParameters
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
