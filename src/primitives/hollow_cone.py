from cadquery import Vector, cq


def hollow_cone(self, top_diameter, bottom_diameter, height, wall):
    _hollow_cone = cq.Solid.makeCone(
        bottom_diameter/2,
        top_diameter/2,
        height
    ).cut(
        cq.Solid.makeCone(
            bottom_diameter/2-wall,
            top_diameter/2-wall,
            height-wall,
        ).translate(Vector(0, 0, wall))
    )

    return self.eachpoint(
        lambda loc: _hollow_cone.locate(loc)
    )
