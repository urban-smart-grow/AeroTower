from cadquery import cq, exporters

outline_width = 70
wall = 2
base_height = 4

piezo_h = 3
piezo_d = 20
piezo_case_h = piezo_h + 6 + wall*2
piezo_case_d = piezo_d + wall*2
filter_d = 8

h = piezo_case_d
l = piezo_case_d
w = outline_width - wall * 2

outline_length = l+wall*2

pump_in_out_gap = 4
pump_case_width = piezo_case_d
tube_d = 4.5
pump_inlet_outline_padding = 1.2
pump_socket_d = pump_in_out_gap+tube_d+pump_inlet_outline_padding
pump_socket_w = 8.5
pump_case_depth = pump_socket_d + wall

wing_depth = 4


mount_points = [
    (-10, 26), (10, 26), (10, -31), (-10, -31)
]


def add_mount_points(self: cq.Workplane):
    return (
        self
        .faces('<Z')
        .workplane(centerOption='CenterOfMass')
        .transformed(rotate=(0, 180, 0))
        .pushPoints(mount_points)
    )


cq.Workplane.add_mount_points = add_mount_points

head_tank = (
    cq.Workplane('XY')
    .box(outline_length, outline_width, h)
    .tag('case')
    # wings
    .faces('>Z', 'case')
    .workplane(centerOption='CenterOfMass')
    .rect(outline_length + wing_depth * 2, outline_width)
    .extrude(-wing_depth-wall)
    .tag('wings')
    .edges('(>X or <X or >Y or <Y) and >>Z[2]')
    .chamfer(wing_depth-0.001)
    # tank hole
    .workplane(offset=wall)
    .box(l, w, h, combine='s')
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
    .move(0, tube_d/2 + wall + pump_inlet_outline_padding)
    .hole(tube_d)
    .edges('|Z')
    .fillet(2)
    .workplaneFromTagged('temp')
    .moveTo(0, wall)
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
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(-7.8, 0, 0))
    .move(0, wall)
    .hole(filter_d, (outline_length + wall)*2 + wall)
    .faces('>Y',  'piezo_socket')
    .tag('filter_hole')
    .workplane(centerOption='CenterOfMass', offset=-wall)
    .move(0, wall)
    .move(0, wall+h)
    .slot2D(h*3, (piezo_d-wall*2), 90)
    .extrude(wall, combine='s')
    .tag('piezo_slot_case')
)

bounding_box = head_tank.combine().objects[0].BoundingBox()


if __name__ == '__main__':
    exporters.export(head_tank, './exports/head_tank.stl')
