from cadquery import cq, exporters
from cq_warehouse.thread import IsoThread
import body
from head_tank import (
    outline_length, outline_width, wing_depth, h as tank_height
)
from head_electronics_lid import lid, pump_spacing
from head_electronics_case import head_electronics_case as case

lid_compound: cq.Compound
lid_compound = lid.combine(
).objects[0]
lid_outline = lid_compound.BoundingBox()

case_compound: cq.Compound
case_compound = case.combine(
).objects[0]
case_outline = case_compound.BoundingBox()


gap = 0.1
wall = 2
socket_height = 16

thread = IsoThread(
    major_diameter=body.top_thread_major_diameter,
    pitch=8,
    length=socket_height,
    external=True,
    end_finishes=('fade', 'fade')
)

outline_width = lid_outline.ylen - wall*4 + gap*2
outline_length = outline_length+gap*2
cutout = (
    cq.Workplane('XY')
    .box(
        outline_length,
        outline_width,
        tank_height,
        centered=(True, True, False)
    )
    .tag('case')
    # wings
    .faces('>Z', 'case')
    .workplane(centerOption='CenterOfMass', offset=wall)
    .rect(outline_length + wing_depth * 2, outline_width)
    .extrude(-wing_depth - wall*2)
    .tag('wings')
    # chamfers
    .edges('(>X or <X or >Y or <Y) and >>Z[2]')
    .chamfer(wing_depth-0.001)
    # fillets
    .edges('|Z')
    .fillet(2)
).combine().objects[0]


head_mount = (
    cq.Workplane('XY').tag('base')
    # base
    .circle(thread.min_radius)
    .extrude(socket_height)
    # lid cutout
    .faces('>Z')
    .workplane()
    .rect(lid_outline.xlen + gap*2, lid_outline.ylen + gap*2)
    .extrude(-wall, combine='s')
    # case cutout
    .faces('>Z')
    .workplane()
    .moveTo(0, pump_spacing/2)
    .rect(case_outline.ylen + gap*2, case_outline.xlen + gap*2)
    .extrude(-wall*2, combine='s')
    # fog cutouts
    .edges('<Z and (<<Y[1] or >>Y[1])')
    .cutEach(
        lambda loc: cq.Solid.makeCone(
            outline_length/2,
            0,
            tank_height
        ).locate(loc)
    )
    # fillets
    .edges('|Z')
    .fillet(2)
    # tank cutout
    .faces('<Z')
    .workplane()
    .cut(cutout.translate((0, 0, socket_height-(tank_height + wall * 2))))
    # thread
    .add(
        thread
    )
)

if __name__ == '__main__':
    exporters.export(head_mount,  './exports/head_mount.stl')
