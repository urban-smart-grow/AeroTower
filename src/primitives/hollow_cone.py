from .cone import cone


def hollow_cone(top_diameter, bottom_diameter, height, wall):
    return (
        cone(
            top_diameter,
            bottom_diameter,
            height
        )
        - cone(
            top_diameter-(wall*2),
            bottom_diameter-(wall*2),
            height-wall,
        ).translate((0, 0, wall))
    )
