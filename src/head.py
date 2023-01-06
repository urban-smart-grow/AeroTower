from cadquery import Vector, cq, exporters

wall = 2

piezo_h = 3
piezo_d = 20
piezo_case_h = piezo_h + 6 + wall*2
piezo_case_d = piezo_d + wall*2
filter_d = 8

h = piezo_case_d
l = piezo_case_d
w = 60

pump_in_out_gap = 3.5
pump_case_width = piezo_case_d
pump_case_depth = 10
tube_d = 4.5
pump_socket_d = pump_in_out_gap+tube_d+1
pump_socket_w = 8.5

head = (
    cq.Workplane('XY')
    .box(l+wall*2, w+wall*2, h)
    .workplane(offset=wall)
    .box(l, w, h, combine='s')
    .tag('case')
    .faces('<Y', 'case')
    .edges('<Z')
    .workplane(
        centerOption='CenterOfMass',
        offset=-pump_case_depth
    )
    .box(
        pump_case_width,
        h,
        pump_case_depth,
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
    .tag('temp')
    .move(0, pump_case_depth - tube_d/2 - pump_in_out_gap)
    .hole(tube_d)
    .edges('|Z')
    .fillet(4)
    .workplaneFromTagged('temp')
    .moveTo(0, pump_case_depth - (pump_socket_d))
    .box(
        pump_socket_w, pump_socket_d, 10,
        combine='s',
        centered=(True, False, True)
    )
    .faces('>Y', 'piezo_socket')
    .workplane(
        offset=wall,
        centerOption='CenterOfMass',
        invert=True
    )
    .move(0, -wall)
    .move(0, -piezo_case_d/2)
    .slot2D(piezo_case_d*2, piezo_d, 90)
    .extrude(piezo_h, combine='s')
    .tag('piezo_slot')
    .faces('>Y',  'piezo_socket')
    .workplane(centerOption='CenterOfMass')
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(-10, 0, 0))
    .move(0, wall)
    .hole(filter_d, piezo_case_h + wall)
    .faces('>Y',  'piezo_socket')
    .tag('filter_hole')
    .workplane(centerOption='CenterOfMass', offset=-wall)
    .move(0, wall)
    .move(0, wall+h)
    .slot2D(h*3, (piezo_d-wall*2), 90)
    .extrude(wall, combine='s')
    .tag('piezo_slot_case')
)


if __name__ == '__main__':
    exporters.export(head, './exports/head.stl')
