import bpy

from ..lens_helpers.materials import get_lens_material
from ..lens_helpers.lens_builder import build_lens
from ..lens_helpers.lens_math import calculate_lens_parameters


class DisplaySpawner(bpy.types.Operator):
    bl_idname = "object.display_spawner"
    bl_label = "Display Spawner"
    bl_description = "Spawns lenses creating the display"

    DISPLAY_WIDTH = 1

    def execute(self, context):
        scene = context.scene
        custom_props = scene.lds_custom_props

        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'

        lens_tilt = custom_props.lds_tilt
        center = custom_props.lds_center
        pitch = custom_props.lds_pitch
        height = custom_props.lds_height
        width = custom_props.lds_width

        # remove old lenses
        for obj in bpy.data.objects:
            if obj.name.startswith("Lens") or obj.name.startswith("Flatten_"):
                bpy.data.objects.remove(obj, do_unlink=True)

        params = calculate_lens_parameters(
            display_width=self.DISPLAY_WIDTH,
            pitch=pitch,
            height=height,
            width=width,
            tilt=lens_tilt,
            center=center
        )

        material = get_lens_material()

        lens = build_lens(params, material)

        # create array
        array_mod = lens.modifiers.new(name="Lens_Array", type='ARRAY')
        array_mod.fit_type = 'FIXED_COUNT'
        array_mod.count = pitch
        array_mod.relative_offset_displace[0] = 1.0001

        return {'FINISHED'}
