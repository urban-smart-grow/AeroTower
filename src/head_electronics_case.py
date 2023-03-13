from cadquery import cq, exporters
from head_tank import add_mount_points
from typing import Callable

bb_width = 58
bb_length = 86
bb_height = 9.5
xiao_height = 7
xiao_cutout = 26
gap = 0.2
wall = 2
cable_hole_d = 4

length = bb_length + wall * 2
width = bb_width + wall * 2
base_height = 2

head_electronics_case = (
    cq.Workplane('XY')
    # base
    .rect(width, length)
    .extrude(base_height)
    .tag('base')
    # border
    .faces('<Z', 'base')
    .rect(width, length)
    .rect(bb_width, bb_length)
    .extrude(bb_height + xiao_height*2)
    # front hole
    .faces('>Y')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass', invert=True)
    .slot2D(xiao_cutout, xiao_height*2)
    .extrude(wall, combine='s')
    # side holes
    .faces('>X')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass')
    .hole(xiao_height * 2)
    # fillets
    .edges('|Z')
    .fillet(2)
)

if __name__ == '__main__':
    exporters.export(head_electronics_case,
                     './exports/head_electronics_case.stl')
