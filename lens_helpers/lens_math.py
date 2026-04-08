import math
from dataclasses import dataclass


@dataclass
class LensParameters:
    radius: float
    height: float
    depth: float
    width_percentage: float
    tilt: float
    center: float
    missing_lenses: int
    vertices: int = 512


def calculate_lens_parameters(
        display_width,
        pitch,
        height,
        width,
        width_percentage,
        depth,
        tilt,
        center,
        vertices=512
):
    tilted_display_width = display_width * math.cos(abs(tilt))

    display_height = (display_width * height) / width

    lens_height = (
            display_width * math.sin(abs(tilt))
            + display_height * math.cos(abs(tilt))
    )

    lens_width = tilted_display_width / pitch

    missing_lenses_width = display_height * math.sin(tilt)
    missing_lenses = math.ceil(missing_lenses_width / lens_width)

    lens_radius = lens_width / (width_percentage * 2 / 100)

    return LensParameters(
        radius=lens_radius,
        height=lens_height,
        depth=depth,
        width_percentage=width_percentage,
        tilt=tilt,
        center=center,
        missing_lenses=missing_lenses,
        vertices=vertices,
    )
