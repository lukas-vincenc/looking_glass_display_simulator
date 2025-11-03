import bpy


class QuiltMakerPanel(bpy.types.Panel):
    bl_label = "Quilt Maker"
    bl_idname = "QUILT_MAKER_PANEL_PT_suffix"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuiltMaker'

    def draw(self, context):
        self.layout.label(text="Spawn Camera Array:")

        self.layout.prop(context.scene, "qm_camera_count")
        self.layout.prop(context.scene, "qm_focus_distance")
        self.layout.prop(context.scene, "qm_focus_object")

        self.layout.separator()
        op = self.layout.operator("object.cameras_spawner", text="Spawn Cameras")

        op.camera_count = context.scene.qm_camera_count
        op.focus_distance = context.scene.qm_focus_distance
        op.focus_object = context.scene.qm_focus_object
