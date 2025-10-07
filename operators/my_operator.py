import bpy

class MY_OT_sample_operator(bpy.types.Operator):
    bl_idname = "myaddon.sample_operator"
    bl_label = "Sample Operator"
    bl_description = "Does something simple"

    def execute(self, context):
        self.report({'INFO'}, "Hello from my add-on!")
        print("Operator executed")
        return {'FINISHED'}
