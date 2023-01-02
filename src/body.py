from cadquery import Location, Vector, Workplane, cq, exporters
from utils.calculate_points_on_circle import calculate_circle_points
import plant_cup

wall = 1
diameter = 160
height = 180


def locate_cone(loc: Location):
    x, y, z = loc.toTuple()[0]

    return (
        cq.Solid.makeCone(
            plant_cup.bottom_diameter/2,
            plant_cup.top_diameter/2,
            plant_cup.height
        )
        .rotate(Vector(0, 0, 0), Vector(-y, x, 0), 45)
        .locate(loc)
    )


def locate_socket(loc: Location):
    x, y, z = loc.toTuple()[0]

    return (
        cq.Solid
        .makeCone(
            plant_cup.bottom_diameter/2 + wall,
            plant_cup.top_diameter/2 + wall,
            plant_cup.height
        )
        .cut(
            cq.Solid
            .makeCone(
                plant_cup.bottom_diameter/2,
                plant_cup.top_diameter/2,
                plant_cup.height
            )
        )
        .rotate(Vector(0, 0, 0), Vector(-y, x, 0), 45)
        .locate(loc)
    )


body = (
    cq.Workplane('XY')
    .circle(diameter/2)
    .circle(diameter/2-wall)
    .extrude(height)
    .workplane(offset=-20)
    .pushPoints(calculate_circle_points(5, height/3))
    .cutEach(locate_cone)
    .pushPoints(calculate_circle_points(5, height/3))
    .eachpoint(locate_socket, combine='a')
    .combine()
    .intersect(
        cq.Solid.makeCylinder(diameter/2, height)
    )
)


exporters.export(body, './exports/body.stl')
