import bpy

QUILT_CAM_TAG = "is_quilt_cam"


def sync_camera_array(context):
    props = context.scene.qm_custom_props
    primary_cam = props.qm_focus_camera
    focus_object = props.qm_focus_object

    if not primary_cam or primary_cam.type != 'CAMERA' or not focus_object:
        return

    count = props.qm_x_views * props.qm_y_views
    spacing = props.qm_spacing

    # Clean up existing quilt cameras
    to_remove = [obj for obj in bpy.data.objects if QUILT_CAM_TAG in obj.keys()]
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    dist = (primary_cam.location - focus_object.location).length

    center_cam = (count - 1) / 2.0

    for i in range(count):
        offset_x = (i - center_cam) * spacing

        new_cam_data = primary_cam.data.copy()
        new_cam_obj = bpy.data.objects.new(f"QuiltCam_{i:03d}", new_cam_data)
        context.collection.objects.link(new_cam_obj)
        new_cam_obj[QUILT_CAM_TAG] = True

        new_cam_obj.parent = primary_cam
        new_cam_obj.location = (offset_x, 0, 0)
        new_cam_obj.rotation_euler = (0, 0, 0)

        sensor_width = primary_cam.data.sensor_width
        focal_length = primary_cam.data.lens

        new_cam_obj.data.shift_x = (-offset_x * focal_length) / (sensor_width * dist)


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "qm.cameras_spawner"
    bl_label = "Reload Cameras Focus"

    def execute(self, context):
        sync_camera_array(context)
        return {'FINISHED'}
