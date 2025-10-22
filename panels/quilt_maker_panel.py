import bpy


class QuiltMakerPanel(bpy.types.Panel):
    bl_label = "Quilt Maker"
    bl_idname = "QUILT_MAKER_PANEL_PT_suffix"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuiltMaker'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.cameras_spawner", text="Spawn Cameras")
