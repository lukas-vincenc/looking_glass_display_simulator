import bpy


class DisplaySimulatorPanel(bpy.types.Panel):
    bl_label = "Lenticular Display Simulator"
    bl_idname = "LENTICULAR DISPLAY SIMULATOR_PT_lds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LentDisplay'

    def draw(self, context):
        self.layout.operator("object.display_spawner", text="Spawn Display")
