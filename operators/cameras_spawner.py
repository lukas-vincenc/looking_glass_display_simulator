import math

import bpy
import mathutils


QUILT_CAMERA_OBJ_NAME = "QuiltCamera"


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "object.cameras_spawner"
    bl_label = "Cameras Spawner"
    bl_description = "Spawns cameras in a line all pointing at a focus point"

    def execute(self, context):
        focus_object = context.scene.qm_focus_object
        focus_distance = context.scene.qm_focus_distance
        camera_count = context.scene.qm_camera_count

        if not focus_object:
            self.report({'ERROR'}, "Please select a focus object")
            return {'CANCELLED'}

        # remove old cameras
        for obj in bpy.data.objects:
            if obj.name.startswith(QUILT_CAMERA_OBJ_NAME):
                bpy.data.objects.remove(obj, do_unlink=True)

        rotation = (math.radians(90), 0, 0)

        for i in range(camera_count):
            location = mathutils.Vector((i - math.floor(camera_count / 2), 0 - focus_distance, 0.0))
            bpy.ops.object.camera_add(location=location, rotation=rotation)
            camera = bpy.context.active_object
            camera.name = f"{QUILT_CAMERA_OBJ_NAME}_{i:03d}"
            camera.parent = focus_object
            camera.data.lens_unit = 'FOV'
            camera.data.angle = math.radians(90)
            camera.data.shift_x = -(i - 22) / float(focus_distance * 2)

        return {'FINISHED'}
