import cadquery as cq


def cone(top_d, bottom_d, height, base=cq.Workplane('XY')):
    return (
        base
        .circle(
            radius=bottom_d/2,
        )
        .workplane(offset=height)
        .circle(radius=top_d/2)
        .loft()
    )
