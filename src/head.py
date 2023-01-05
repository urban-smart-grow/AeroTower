from cadquery import Vector, cq, exporters

wall = 2

piezo_h = 3
piezo_d = 20
piezo_case_h = piezo_h + wall*2
piezo_case_d = piezo_d + wall*2

h = piezo_d + wall * 2
l = 100
w = 100

head = (
    cq.Workplane('XY')
    .box(l+wall*2, w+wall*2, h)
    .workplane(offset=wall)
    .box(l, w, h, combine='s')
    .edges('|Z')
    .fillet(4)
    .tag('case')
    .faces('<Y', 'case')
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
    .tag('pump_socket')
    .faces('>Y', 'case')
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
    .tag('piezo_socket')
    .faces('>Z', 'case')
    .edges('<Y')
    .workplane(centerOption='CenterOfMass')
    .move(0, piezo_case_h/2)
    .hole(4)
    .edges('|Z')
    .fillet(2)
    .faces('>Y',  'piezo_socket')
    .workplane(centerOption='CenterOfMass')
    .hole(6, piezo_case_h)
    .faces('>Y', 'piezo_socket')
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
