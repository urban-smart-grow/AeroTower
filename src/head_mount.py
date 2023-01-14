from cadquery import cq, exporters
from cq_warehouse.thread import IsoThread
import body
from head_tank import head
from head_electronics_lid import lid

head_tank_compound: cq.Compound
head_tank_compound = head.combine().objects[0]
tank_outline = (
    head_tank_compound.BoundingBox()
)

lid_compound: cq.Compound
lid_compound = lid.combine(
).objects[0]
lid_outline = lid_compound.BoundingBox()


gap = 0.6
wall = 2
socket_height = tank_outline.zlen + wall

thread = IsoThread(
    major_diameter=body.top_thread_major_diameter,
    pitch=8,
    length=socket_height,
    external=True,
    end_finishes=('fade', 'fade')
)

head_mount = (
    cq.Workplane('XY')
    .circle(thread.min_radius)
    .rect(
        tank_outline.xlen + gap,
        tank_outline.ylen + gap,
    )
    .extrude(socket_height)
    .faces('+Z')
    .workplane(offset=-wall)
    .rect(lid_outline.xlen + gap, lid_outline.ylen + gap)
    .extrude(wall, combine='s')
    .edges('<Z and (<<Y[1] or >>Y[1])')
    .cutEach(
        lambda loc: cq.Solid.makeCone(
            tank_outline.xlen/2,
            0,
            tank_outline.zlen
        ).locate(loc)
    )
    .edges('|Z')
    .fillet(2)
    .add(
        thread
    )
)

if __name__ == '__main__':
    exporters.export(head_mount, './exports/head_mount.stl')
