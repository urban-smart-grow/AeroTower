from cadquery import Vector, cq, exporters
import head_electronics_case as case

wall = 2
height = 40

outer_xy = (case.length + wall * 2, case.width + wall * 2)

cutout = tuple(map(lambda x: x*2, case.battery_mount_outline))

lid = (
    cq.Workplane('XY')
    .rect(*outer_xy)
    .rect(case.length, case.width)
    .extrude(height)
    .faces('<Z')
    .rect(*outer_xy)
    .extrude(wall)
    .edges('|Z')
    .fillet(2)
    .faces('>Y')
    .edges('>Z')
    .workplane(centerOption='CenterOfMass', invert=True)
    .slot2D(10, 8)
    .extrude(case.width + wall * 2, combine='s')
    .add(
        cq.Workplane('XY')
        .rect(case.length, case.width)
        .rect(case.length - wall*2, case.width - wall*2)
        .extrude(height - case.base_height)
        .tag('inner_base')
        .edges('|Z')
        .fillet(2)
        .vertices('>Z', 'inner_base')
        .box(*cutout, combine='s', centered=True)
    )
)
exporters.export(lid, './exports/head_electronics_lid.stl')
