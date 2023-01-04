from cadquery import Vector, cq, exporters

l = 100
w = 60
h = 24
wall = 2
piezo_h = 3
piezo_d = 20
piezo_case_h = piezo_h + wall*2
piezo_case_d = piezo_d + wall*2

head = (
    cq.Workplane('XY')
    .box(l+wall*2, w+wall*2, h)
    .workplane(offset=wall)
    .box(l, w, h, combine='s')
    .edges('|Z')
    .fillet(4)
    .faces('>Y')
    .edges('<Z')
    .workplane(
        centerOption='CenterOfMass',
        offset=-piezo_case_h
    )
    .box(
        piezo_case_d,
        h,
        piezo_case_h,
        centered=(True, False, False),
    )
    .edges('|Z')
    .fillet(2)
    .faces('>Y')
    .workplane(centerOption='CenterOfMass')
    .hole(6, piezo_case_h)
    .faces('>Y')
    .workplane(
        offset=wall,
        centerOption='CenterOfMass',
        invert=True
    )
    .move(0, -piezo_case_d/2)
    .slot2D(piezo_case_d*2, piezo_d, 90)
    .extrude(piezo_h, combine='s')
)


if __name__ == '__main__':
    exporters.export(head, './exports/head.stl')
