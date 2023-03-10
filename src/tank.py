from cadquery import Vector, cq, exporters
from cq_warehouse.thread import IsoThread
from primitives.hollow_cone import hollow_cone

diameter = 180
height = 180
wall = 2
socket_height = 20
pitch = 8

thread_major_diameter = diameter-wall*2
thread = IsoThread(
    major_diameter=thread_major_diameter,
    pitch=pitch,
    length=socket_height,
    external=False,
    end_finishes=('fade', 'fade')
)

thread = thread.cq_object.translate(Vector(0, 0, height-socket_height))

cq.Workplane.hollow_cone = hollow_cone

tank = thread.fuse(
    cq.Solid.makeCylinder(diameter/2, height)
    .cut(
        cq.Solid.makeCylinder(diameter/2-wall, height-wall)
        .translate(Vector(0, 0, wall))
    )
)

print('_'*30)
print(__name__)
print(f'{thread_major_diameter=}')
print('_'*30)

exporters.export(tank, './exports/tank.stl')
