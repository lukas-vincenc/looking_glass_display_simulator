import bpy

QUILT_CAM_TAG = "QM_Child"


def sync_camera_array(context):
    props = context.scene.qm_custom_props
    source_cam = props.qm_focus_camera
    focus_object = props.qm_focus_object

    # Validation
    if not source_cam or source_cam.type != 'CAMERA' or not focus_object:
        return

    count = props.qm_x_views * props.qm_y_views
    spacing = props.qm_spacing
    QUILT_CAM_TAG = "is_quilt_cam"  # Ensure this is defined

    # Cleanup existing array cameras
    to_remove = [obj for obj in bpy.data.objects if QUILT_CAM_TAG in obj.keys()]
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Calculate distance (Focal Plane)
    # Use world matrices to find the true distance along the camera's Z-axis
    cam_matrix = source_cam.matrix_world
    obj_matrix = focus_object.matrix_world

    # Distance from camera plane to object
    # This is more robust than simple .length if the camera isn't pointed directly at the object
    rel_pos = cam_matrix.inverted() @ obj_matrix.translation
    dist_to_plane = abs(rel_pos.z)

    middle = (count - 1) / 2.0

    for i in range(count):
        offset_x = (i - middle) * spacing

        # Create new camera
        new_cam_data = source_cam.data.copy()
        new_cam_obj = bpy.data.objects.new(f"QuiltCam_{i:03d}", new_cam_data)
        context.collection.objects.link(new_cam_obj)
        new_cam_obj[QUILT_CAM_TAG] = True

        # Setup Hierarchy
        new_cam_obj.parent = source_cam
        new_cam_obj.location = (offset_x, 0, 0)
        new_cam_obj.rotation_euler = (0, 0, 0)

        # Calculate Lens Shift
        # Formula: shift = -offset / (sensor_width * (dist_to_plane / focal_length))
        # But Blender's shift_x is relative to the longest side of the sensor.
        # Simplified: shift_x = -offset / sensor_width_at_focal_plane

        sensor_width = source_cam.data.sensor_width
        focal_length = source_cam.data.lens

        # This calculates how many 'sensor widths' the offset represents at the focus distance
        new_cam_obj.data.shift_x = (-offset_x * focal_length) / (sensor_width * dist_to_plane)


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "qm.cameras_spawner"
    bl_label = "Reload Cameras Focus"

    def execute(self, context):
        sync_camera_array(context)
        return {'FINISHED'}
