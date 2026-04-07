import math

import bpy
from bpy.props import FloatProperty

from .scene_spawner import SceneSpawner


def update_ray_source_x(self, context):
    obj = bpy.data.objects.get("Ray_Source")
    if obj is None:
        return

    obj.location.x = self.ray_source_x / 10


def update_ray_source_rotation(self, context):
    obj = bpy.data.objects.get("Ray_Source")
    if obj is None:
        return

    obj.rotation_euler.z = self.ray_source_rotation


class CustomProps(bpy.types.PropertyGroup):
    ray_source_x: FloatProperty(
        name="Ray Source X",
        default=0.0,
        subtype='DISTANCE',
        update=update_ray_source_x
    )
    ray_source_rotation: FloatProperty(
        name="Ray Source Rotation",
        default=math.pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_ray_source_rotation
    )
    lens_depth: FloatProperty(
        name="Lens Depth",
        default=3,
        unit='NONE'
    )


class LensVisualizationPanel(bpy.types.Panel):
    bl_label = "Lens Visualization"
    bl_idname = "LENS_VISUALIZATION_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LensVisualization'

    def draw(self, context):
        layout = self.layout
        cus_pt = context.scene.lvis_custom_props

        layout.prop(cus_pt, "ray_source_x")
        layout.prop(cus_pt, "ray_source_rotation")
        layout.prop(cus_pt, "lens_depth")

        layout.operator("object.scene_spawner", text="Spawn Scene")


all_classes = [
    CustomProps,
    LensVisualizationPanel,
    SceneSpawner
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lvis_custom_props = bpy.props.PointerProperty(type=CustomProps)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lvis_custom_props
