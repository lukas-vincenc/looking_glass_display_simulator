import math
from dataclasses import dataclass


@dataclass
class LensParameters:
    radius: float
    height: float
    tilt: float
    center: float
    vertices: int = 512


def calculate_lens_parameters(
        display_width,
        pitch,
        height,
        width,
        tilt,
        center,
        vertices=512
):
    tilted_display_width = display_width * math.cos(abs(tilt))

    lens_height = (
        display_width * math.sin(abs(tilt))
        + (height / width) * math.cos(abs(tilt))
    )

    lens_radius = (tilted_display_width / pitch / 2) * (3 / 2)

    return LensParameters(
        radius=lens_radius,
        height=lens_height,
        tilt=tilt,
        center=center,
        vertices=vertices
    )
