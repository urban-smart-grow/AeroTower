from cadquery import Vector, cq


def drop_cut(side_length: float):
    drop_cut = (
        cq.Solid.makeBox(side_length, side_length/2,
                         side_length, Vector(-side_length/2, 0, 0))
        .cut(
            cq.Solid.makeCylinder(side_length/2, side_length,
                                  Vector(side_length/2, side_length/2, 0))
        )
        .cut(
            cq.Solid.makeCylinder(side_length/2, side_length,
                                  Vector(-side_length/2, side_length/2, 0))
        )
        .rotate(Vector(), Vector(1, 0, 0), 90)
        .rotate(Vector(), Vector(0, 0, 1), -90)
    )
    return drop_cut
