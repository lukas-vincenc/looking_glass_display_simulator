import bpy

from .lens_geometry_nodes import get_node_tree, update_gn_pitch
from ..lens_helpers.materials import get_lens_material, get_block_material
from ..lens_helpers.lens_builder import build_lens, set_origin_bottom_center
from ..lens_helpers.lens_math import calculate_lens_parameters


def get_refractive_block(custom_props, display_width):
    block_height = custom_props.lds_height / (custom_props.lds_width * display_width)
    block_depth = custom_props.lds_block_depth

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0.5, -0.5, 0.5),
    )

    block = bpy.context.object
    block.name = "RefractiveBlock"

    set_origin_bottom_center(block)

    block.scale.y = block_depth
    block.scale.z = block_height

    material = get_block_material()
    block.data.materials.append(material)

    return block


def clear_scene():
    prefixes = ("RefractiveBlock", "Lens", "Flatten")
    for obj in bpy.data.objects:
        if obj.name.startswith(prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)


class DisplaySpawner(bpy.types.Operator):
    bl_idname = "object.display_spawner"
    bl_label = "Display Spawner"
    bl_description = "Spawns lenses creating the display"

    DISPLAY_WIDTH = 1

    def execute(self, context):
        scene = context.scene
        custom_props = scene.lds_custom_props

        # Render engine needs to be Cycles - simulates refraction
        # GPU is a nice performance bonus - if Blender doesn't have a supported GPU selected, it stays on CPU on its own
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'

        clear_scene()

        params = calculate_lens_parameters(
            display_width=self.DISPLAY_WIDTH,
            pitch=custom_props.lds_pitch,
            height=custom_props.lds_height,
            width=custom_props.lds_width,
            depth=custom_props.lds_depth,
            width_percentage=custom_props.lds_lens_width,
            tilt=custom_props.lds_tilt,
            center=custom_props.lds_center
        )

        material = get_lens_material()
        lens = build_lens(params, material, self.DISPLAY_WIDTH)

        gn_tree = get_node_tree()
        gn_mod = lens.modifiers.new(name="LDS_GeometryNodes", type='NODES')
        gn_mod.node_group = gn_tree
        update_gn_pitch(gn_mod, custom_props.lds_pitch, params.missing_lenses)

        get_refractive_block(custom_props, self.DISPLAY_WIDTH)

        return {'FINISHED'}
