import bpy


# Called when "View Primary Camera" is pressed
# Switches the main viewport to primary camera's POV
class PrimaryCameraSelector(bpy.types.Operator):
    bl_idname = "qm.view_primary_camera"
    bl_label = "View Primary Camera"
    bl_description = "Switch view to the Primary Camera's POV"

    def execute(self, context):
        props = context.scene.qm_custom_props
        source_cam = props.qm_focus_camera

        if not source_cam:
            self.report({'WARNING'}, "No Primary Camera selected!")
            return {'CANCELLED'}

        # Set the scene's active camera
        context.scene.camera = source_cam

        # Force the 3D Viewport to look through the camera
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'

        return {'FINISHED'}
