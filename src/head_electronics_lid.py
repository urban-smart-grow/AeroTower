from cadquery import Vector, cq, exporters
import head_electronics_case as case


bb_width = 57
bb_length = 85
height = 30
xiao_height = 7
xiao_cutout = 26
gap = 0.2
wall = 2

length = bb_length + (gap + wall) * 2
width = bb_width + (gap + wall) * 2
base_height = wall


lid = (
    cq.Workplane('XY')
    .rect(bb_width, bb_length)
    .rect(bb_width - wall, bb_length - wall)
    .extrude(base_height + height - xiao_height)
    .faces('<Z')
    .rect(bb_width, bb_length)
    .rect(width, length)
    .extrude(height + base_height)
    .faces('<Z')
    .rect(width, length)
    .extrude(base_height)
    .faces('<<Y[1]')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass', invert=True)
    .slot2D(xiao_cutout, xiao_height*2)
    .extrude(wall*2, combine='s')
    .faces('>X')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass')
    .hole(xiao_height * 2)
    .edges('|Z')
    .fillet(2)
)

exporters.export(lid, './exports/head_electronics_lid.stl')
