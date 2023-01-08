from cadquery import cq, exporters

mount_points = [
    # Xiao with extension board
    (55, 5), (75, 5), (75, 40), (55, 40),
    # Atomizer
    (35, 20), (35, 40), (5, 30),
    # Pump/Mosfet
    (35, 45), (35, 65), (5, 55),
]

head_electronics_case = (
    cq.Workplane('XY')
    .box(80, 70, 4, centered=False)
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
    .faces('<Z', 'base')
    .workplane(centerOption='CenterOfMass')
    .box(84, 74, 2, centered=(True, True, False))
    .edges('|Z')
    .fillet(2)
)

if __name__ == '__main__':
    exporters.export(head_electronics_case,
                     './exports/head_electronics_case.stl')
