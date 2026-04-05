import bpy

QUILT_CAM_TAG = "QM_Child"


def sync_camera_array(context):
    props = context.scene.qm_custom_props
    source_cam = props.qm_focus_camera

    if not source_cam or source_cam.type != 'CAMERA':
        return

    count = props.qm_x_views * props.qm_y_views
    spacing = props.qm_spacing

    to_remove = [obj for obj in bpy.data.objects if QUILT_CAM_TAG in obj]
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    middle = (count - 1) / 2.0

    # TODO: fix focal length
    focal_len = source_cam.data.lens

    for i in range(count):

        offset_x = (i - middle) * spacing

        new_cam_data = source_cam.data.copy()
        new_cam_obj = bpy.data.objects.new(f"QuiltCam_{i:03d}", new_cam_data)
        context.collection.objects.link(new_cam_obj)

        new_cam_obj[QUILT_CAM_TAG] = True

        new_cam_obj.parent = source_cam

        new_cam_obj.location = (offset_x, 0, 0)
        new_cam_obj.rotation_euler = (0, 0, 0)

        new_cam_obj.data.shift_x = -offset_x / focal_len


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "qm.cameras_spawner"
    bl_label = "Force Sync Cameras"

    def execute(self, context):
        sync_camera_array(context)
        return {'FINISHED'}
