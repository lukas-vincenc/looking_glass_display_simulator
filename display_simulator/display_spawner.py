import bpy

from .lens_geometry_nodes import get_node_tree
from ..lens_helpers.materials import get_lens_material, get_block_material
from ..lens_helpers.lens_builder import build_lens
from ..lens_helpers.lens_math import calculate_lens_parameters


def get_refractive_block(custom_props, display_width, lens_depth):
    block_height = custom_props.lds_height / (custom_props.lds_width * display_width)
    block_depth = 0.1

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0.5, (-block_depth / 2) - lens_depth, block_height / 2)
    )

    block = bpy.context.object
    block.name = "RefractiveBlock"

    block.scale.y = block_depth
    block.scale.z = block_height

    material = get_block_material()
    block.data.materials.append(material)

    return block


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
        lens_width_percentage = custom_props.lds_lens_width
        depth = custom_props.lds_depth

        # remove old lenses
        for obj in bpy.data.objects:
            if obj.name.startswith("Lens") or obj.name.startswith("Flatten_") or obj.name.startswith("RefractiveBlock"):
                bpy.data.objects.remove(obj, do_unlink=True)

        params = calculate_lens_parameters(
            display_width=self.DISPLAY_WIDTH,
            pitch=pitch,
            height=height,
            width=width,
            depth=depth,
            width_percentage=lens_width_percentage,
            tilt=lens_tilt,
            center=center
        )

        material = get_lens_material()

        lens = build_lens(params, material)

        gn_tree = get_node_tree()

        gn_mod = lens.modifiers.new(name="LDS_GeometryNodes", type='NODES')
        gn_mod.node_group = gn_tree

        pitch_identifier = None
        for item in gn_mod.node_group.interface.items_tree:
            if item.name == "Pitch" and item.in_out == 'INPUT':
                pitch_identifier = item.identifier
                break

        if pitch_identifier:
            gn_mod[pitch_identifier] = pitch

        extra_lenses_identifier = None
        for item in gn_mod.node_group.interface.items_tree:
            if item.name == "Extra Lenses" and item.in_out == 'INPUT':
                extra_lenses_identifier = item.identifier
                break

        if extra_lenses_identifier:
            gn_mod[extra_lenses_identifier] = params.missing_lenses

        get_refractive_block(custom_props, self.DISPLAY_WIDTH, params.depth * params.radius)

        return {'FINISHED'}
