import math

import bpy
import mathutils


QUILT_CAMERA_OBJ_NAME = "QuiltCamera"


class CamerasSpawner(bpy.types.Operator):
    bl_idname = "qm.cameras_spawner"
    bl_label = "Spawn Cameras"
    bl_description = "Spawns cameras in a line all pointing at a focus point"

    def execute(self, context):
        scene = context.scene
        custom_props = scene.custom_props
        shared_storage = scene.shared_storage

        # TODO: temp, to handle better
        scene = bpy.context.scene
        scene.render.resolution_x = 500
        scene.render.resolution_y = 500
        scene.render.resolution_percentage = 100

        focus_object = custom_props.qm_focus_object
        focus_distance = custom_props.qm_focus_distance
        camera_count = custom_props.qm_camera_count

        if not focus_object:
            self.report({'ERROR'}, "Please select a focus object")
            return {'CANCELLED'}

        # remove old cameras
        for obj in bpy.data.objects:
            if obj.name.startswith(QUILT_CAMERA_OBJ_NAME):
                bpy.data.objects.remove(obj, do_unlink=True)

        rotation = (math.radians(90), 0, 0)
        middle = math.floor(camera_count / 2)

        for i in range(camera_count):
            location = mathutils.Vector((i - middle, -focus_distance, 0.0))
            bpy.ops.object.camera_add(location=location, rotation=rotation)
            camera = bpy.context.active_object

            cam_name = f"{QUILT_CAMERA_OBJ_NAME}_{i:03d}"
            camera.name = cam_name
            camera.parent = focus_object

            camera.data.lens_unit = 'FOV'
            camera.data.angle = math.radians(90)
            camera.data.shift_x = -(i - 22) / float(focus_distance * 2)

            item = shared_storage.camera_names.add()
            item.value = cam_name

        self.report({'INFO'}, "Spawning cameras complete")
        return {'FINISHED'}
