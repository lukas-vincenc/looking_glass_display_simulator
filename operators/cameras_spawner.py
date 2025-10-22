import math

import bpy
import mathutils


QUILT_CAMERA_OBJ_NAME = "QuiltCamera"


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "object.cameras_spawner"
    bl_label = "Cameras Spawner"
    bl_description = "Spawns cameras in a line all pointing at a focus point"

    def execute(self, context):
        camera_count = 10
        spacing = 1.0
        camera_distance = 10.0
        focus_point = mathutils.Vector((0.0, 0.0, 0.0))

        # remove old cameras
        for obj in bpy.data.objects:
            if obj.name.startswith(QUILT_CAMERA_OBJ_NAME):
                bpy.data.objects.remove(obj, do_unlink=True)

        rotation = (math.radians(90), 0, 0)

        # Compute horizontal field of view
        # Assume all cameras use default sensor size and focal length
        base_cam_data = bpy.data.cameras.new("TempCamData")
        fov_x = base_cam_data.angle_x  # radians
        bpy.data.cameras.remove(base_cam_data)

        # Center offset
        half = (camera_count - 1) / 2.0

        for i in range(camera_count):
            x = i * spacing - half * spacing
            location = mathutils.Vector((x, -camera_distance, 0))

            bpy.ops.object.camera_add(location=location)
            cam = bpy.context.object
            cam.name = f"{QUILT_CAMERA_OBJ_NAME}_{i:03d}"
            cam.rotation_euler = rotation

            # TODO: this computation is incorrect
            shift_x = -x / (camera_distance * math.tan(fov_x / 2))
            cam.data.shift_x = shift_x

        return {'FINISHED'}
