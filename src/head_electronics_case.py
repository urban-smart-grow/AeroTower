from cadquery import cq, exporters
from head_tank import add_mount_points

length = 100
width = 70


cq.Workplane.add_mount_points = add_mount_points

mount_points = [
    # Xiao with extension board
    (67.5, 5), (87.5, 5), (87.5, 40), (67.5, 40),
    # Atomizer
    (35, 20), (35, 40), (5, 30),
    # Pump/Mosfet
    (35, 45), (35, 65), (5, 55),
]

head_electronics_case = (
    cq.Workplane('XY')
    .box(length, width, 4, centered=False)
    .tag('base')
    .faces('>Z')
    .workplane()
    .pushPoints(mount_points)
    .circle(2)
    .extrude(2)
    .pushPoints(mount_points)
    .circle(1)
    .extrude(5)
    .faces('>Z', 'base')
    .vertices('<XY')
    .workplane(centerOption='CenterOfMass').tag('battery_mount')
    .box(40, 16, 14, centered=False)
    .workplaneFromTagged('battery_mount')
    .center(0, 5)
    .box(40, 6, 14, centered=False, combine='s')
    .faces('>Z', 'base')
    .workplane(centerOption='CenterOfMass', offset=-2)
    .box(
        10, width, 2,
        centered=(True, True, False),
        combine='s'
    )
    .tag('wire_channel')
    .faces('>Z', 'base')
    .edges('<Y')
    .workplane(centerOption='CenterOfMass', offset=-4)
    .box(
        10, 6, 4,
        centered=(True, False, False),
        combine='s'
    )
    .tag('wire_outlet')
    .edges('|Z')
    .fillet(2)
    .faces('>Z', 'base')
    .edges('>Y')
    .workplane(centerOption='CenterOfMass', offset=-4)
    .move(0, -20.6)
    .box(
        8.6, 18.6, 4,
        centered=(True, False, False),
        combine='s'
    )
    .tag('pump_hole')
    .translate((-length/2, -width/2, 0))
    .add_mount_points()
    .circle(2).extrude(2, combine='s')
)

if __name__ == '__main__':
    exporters.export(head_electronics_case,
                     './exports/head_electronics_case.stl')
