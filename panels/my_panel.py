import bpy

class MY_PT_sample_panel(bpy.types.Panel):
    bl_label = "Lenticular Display Simulator"
    bl_idname = "Lenticular Display Simulator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LentDisplay'

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.sample_operator", text="Run Operator")
