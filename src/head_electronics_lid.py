from cadquery import cq, exporters
from head_electronics_case import (
    head_electronics_case as case,
    cable_hole_d,  bb_width, bb_length,
    length, width, gap, xiao_cutout, xiao_height
)


height = 16
wall = 2

shell_length = length + wall * 2
shell_width = width + wall * 4
base_height = wall
pump_spacing = 24

case_bounding_box = case.combine().objects[0].BoundingBox()

lid = (
    cq.Workplane('XY')
    # base
    .rect(width, length)
    .extrude(base_height)
    .tag('base')
    # outer boarder
    .faces('<Z', 'base')
    .rect(shell_width + pump_spacing, shell_length)
    .rect(width - gap*2 + pump_spacing, length - gap*2)
    .extrude(height + case_bounding_box.zlen)
    .tag('outer border')
    # base extension
    .faces('<Z', 'base')
    .rect(shell_width + pump_spacing, shell_length)
    .extrude(base_height)
    # cable hole
    .faces('>Z')
    .edges('<<X[1]')
    .hole(cable_hole_d,  case_bounding_box.zlen)
    # fillets
    .edges('|Z')
    .fillet(2)
    # slot
    .faces('<Y')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass')
    .moveTo(pump_spacing/2, 0)
    .rect(xiao_cutout, height*2)
    .extrude('last', 'cut')
    .moveTo(pump_spacing/2, -height)
    .slot2D(xiao_cutout, xiao_height*2)
    .extrude('last', 'cut')


)

outline = lid.combine().objects[0].BoundingBox()

print(f'{outline.xlen:0.2f}, {outline.ylen:0.2f}, {outline.zlen:0.2f}')

exporters.export(lid, './exports/head_electronics_lid.stl')
