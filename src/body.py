from cadquery import Location, Vector, cq, exporters
from utils.calculate_points_on_circle import calculate_circle_points
import plant_cup
import time

wall = 1
diameter = 160
height = 150
number_of_cup_holders = 5


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


start = time.time()

body = (
    cq.Workplane('XY')
    .circle(diameter/2)
    .circle(diameter/2-wall)
    .extrude(height)
    .workplane(offset=-20)
    .pushPoints(calculate_circle_points(number_of_cup_holders, diameter/3))
    .cutEach(locate_cone)
    .pushPoints(calculate_circle_points(number_of_cup_holders, diameter/3))
    .eachpoint(locate_socket, combine='a')
    .combine()
    .intersect(
        cq.Solid.makeCylinder(diameter/2, height)
    )
)

end = time.time()

print(f'took {end-start:0.2f} seconds')

if __name__ == '__main__':
    exporters.export(body, './exports/body.stl')
