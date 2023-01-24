from cadquery import cq, exporters
from head_tank import add_mount_points
from typing import Callable

bb_width = 57
bb_length = 85
bb_height = 9.5
xiao_height = 7
xiao_cutout = 26
gap = 0.2
wall = 2

length = bb_length + (gap + wall) * 2
width = bb_width + (gap + wall) * 2
base_height = wall * 2

head_electronics_case = (
    cq.Workplane('XY')
    .rect(width, length)
    .rect(bb_width, bb_length)
    .extrude(bb_height + base_height)
    .faces('<Z')
    .rect(width, length)
    .extrude(base_height)
    .faces('>Z')
    .rect(bb_width + wall, bb_length + wall)
    .rect(bb_width, bb_length)
    .extrude(xiao_height)
    .faces('<<Y[2]')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass', invert=True)
    .slot2D(xiao_cutout, xiao_height*2)
    .extrude(wall, combine='s')
    .faces('>>X[-2]')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass')
    .hole(xiao_height * 2)
    .edges('|Z')
    .fillet(2)
)

if __name__ == '__main__':
    exporters.export(head_electronics_case,
                     './exports/head_electronics_case.stl')
