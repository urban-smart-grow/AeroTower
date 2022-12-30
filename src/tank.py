from cadquery import Vector, cq, exporters
from cq_warehouse.thread import IsoThread
from primitives.hollow_cone import hollow_cone

diameter = 180
height = 180
wall = 2
socket_height = 20
pitch = 8

thread = IsoThread(
    major_diameter=diameter-wall,
    pitch=pitch,
    length=socket_height,
    external=False,
    end_finishes=('fade', 'fade')
).cq_object.translate(Vector(0, 0, height-socket_height))

tank = thread.fuse(
    hollow_cone(diameter, diameter, height, wall).val()
)

exporters.export(tank, './exports/tank.stl')
