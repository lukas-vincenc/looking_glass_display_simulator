import bpy

from .scene_spawner import SceneSpawner


class LensVisualizationPanel(bpy.types.Panel):
    bl_label = "Lens Visualization"
    bl_idname = "LENS VISUALIZATION_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LensVisualization'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.scene_spawner", text="Spawn Scene")


all_classes = [
    LensVisualizationPanel,
    SceneSpawner
]


def register():
    for cls in all_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in all_classes:
        bpy.utils.unregister_class(cls)
