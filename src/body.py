import math
from cadquery import Location, Vector, cq, exporters
from primitives.drop_cut import drop_cut
from primitives.hollow_cone import hollow_cone
from utils.calculate_points_on_circle import calculate_circle_points
from cq_warehouse.thread import IsoThread
import plant_cup
import time

wall = 1
diameter = 160
height = 164
number_of_cup_holders = 5
cup_angle = 45
socket_height = 20
pitch = 8

socket_offset = (diameter)/2 - (
    math.cos(math.radians(cup_angle))
    * (plant_cup.bottom_diameter/2+wall)
)

points = list(
    calculate_circle_points(
        number_of_cup_holders,
        socket_offset
    )
)

cq.Workplane.hollow_cone = hollow_cone


def locate_cone(loc: Location):
    x, y, z = loc.toTuple()[0]

    return (
        cq.Solid.makeCone(
            plant_cup.bottom_diameter/2,
            plant_cup.top_diameter/2,
            plant_cup.height
        )
        .rotate(Vector(), Vector(-y, x, 0), cup_angle)
        .locate(loc)
    )


def locate_socket(loc: Location):
    x, y, z = loc.toTuple()[0]
    angle = math.degrees(math.atan2(y, x))

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
        .cut(drop_cut(plant_cup.bottom_diameter))
        .rotate(Vector(), Vector(0, 0, 1), angle)
        .rotate(Vector(), Vector(-y, x, 0), cup_angle)
        .locate(loc)
    )


start = time.time()
top_thread_major_diameter = diameter-(wall*2)
top_thread = IsoThread(
    major_diameter=top_thread_major_diameter,
    pitch=pitch-0.2,
    length=socket_height,
    external=False,
    end_finishes=('fade', 'fade')
)

top_thread_min_radius = top_thread.min_radius

top_thread = top_thread.cq_object.translate(Vector(0, 0, height-socket_height))

bottom_thread_major_diameter = diameter-(wall*2)

bottom_thread = IsoThread(
    major_diameter=bottom_thread_major_diameter,
    pitch=pitch,
    length=socket_height,
    external=True,
    end_finishes=('fade', 'fade')
)

thread_body_radius_delta = (
    diameter / 2
    - bottom_thread.min_radius
)

thread_body_transition_height = thread_body_radius_delta*2

bottom_thread_min_radius = bottom_thread.min_radius

bottom_thread = bottom_thread.fuse(
    cq.Workplane('XY')
    .circle(bottom_thread.min_radius)
    .circle(bottom_thread.min_radius - wall)
    .extrude(socket_height)
    .val()
)

body = (
    cq.Workplane('XY', origin=Vector(
        0, 0, (socket_height+(thread_body_transition_height))
    ))
    .circle(diameter/2)
    .circle(diameter/2-wall)
    .extrude(height-(socket_height+thread_body_radius_delta))
    .workplane(offset=-20)
    .pushPoints(points)
    .cutEach(locate_cone)
    .pushPoints(points)
    .eachpoint(locate_socket, combine='a')
    .add(top_thread)
    .add(bottom_thread)
    .add(
        cq.Workplane('XY', origin=Vector(0, 0, socket_height))
        .hollow_cone(
            diameter,
            bottom_thread_min_radius*2,
            thread_body_transition_height,
            wall,
            bottom=0
        )
    )
    .combine()
    .intersect(
        cq.Solid.makeCylinder(diameter/2, height)
    )
)


end = time.time()


print(f'took {end-start:0.2f} seconds')

if __name__ == '__main__':
    exporters.export(body, './exports/body.stl')
