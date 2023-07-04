from cadquery import cq, exporters
from cq_warehouse.thread import IsoThread
import body
from head_tank import (
    outline_length, outline_width, wing_depth, h as tank_height
)
from head_electronics_lid import lid, pump_spacing
from head_electronics_case import head_electronics_case as case
from constants import thread_gap_in_mm

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
layer_height = 4

thread_major_diameter = body.top_thread_major_diameter - (thread_gap_in_mm*2)

thread = IsoThread(
    major_diameter=thread_major_diameter,
    pitch=8,
    length=socket_height,
    external=True,
    end_finishes=('fade', 'fade')
)

outline_width = outline_width + gap*2
outline_length = outline_length+gap*2
lid_outline_width = lid_outline.ylen - wall*4 + gap*2
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
    .workplane(centerOption='CenterOfMass', offset=layer_height)
    .rect(outline_length + wing_depth * 2, outline_width)
    .extrude(-wing_depth - layer_height*2)
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
    .extrude(-layer_height, combine='s')
    # case cutout
    .faces('>Z')
    .workplane()
    .moveTo(0, pump_spacing/2)
    .rect(case_outline.ylen + gap*2, case_outline.xlen + gap*2)
    .extrude(-layer_height*2, combine='s')
    # tank cutout
    .faces('<Z')
    .workplane()
    .cut(
        cutout
        .translate((
            0,
            -(lid_outline_width-outline_width)/2,
            socket_height-(tank_height + layer_height * 2)
        )
        ))
    # fillets
    .edges('|Z')
    .fillet(2)
    # tunnel
    .box(
        outline_length,
        lid_outline_width,
        socket_height*2,
        combine='s'
    )
    # piezo cable hole
    .workplaneFromTagged('base')
    .move(0, lid_outline_width/2)
    .circle(2).extrude(50, 'cut')
    # thread
    .add(
        thread
    )
)


print('_'*30)
print(__name__)
print(f'{thread_major_diameter=}')
print('_'*30)

if __name__ == '__main__':
    exporters.export(head_mount,  './exports/head_mount.stl')
