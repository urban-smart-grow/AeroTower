from cadquery import cq, exporters
# import head_mount, head_electronics_lid, body
# import math

wall = 2
body_overlap = 4
gap = 0.4
body_diameter = 160 # body.diameter
body_radius = body_diameter / 2
outer_radius = body_radius + wall
inner_radius = body_radius + gap

electronics_case_outstand = 36
# electronics_case_outstand = math.ceil(
#      head_electronics_lid.lid.combine().objects[0].BoundingBox().zlen 
#      - head_mount.layer_height
# )
height = electronics_case_outstand + body_overlap

solar_module_case = (
    cq.Workplane('XY')
    .tag('base')
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
    .workplaneFromTagged('base')
    .circle(inner_radius)
    .circle(body_radius-wall)
    .extrude(electronics_case_outstand)
    .workplaneFromTagged('base')
    .circle(outer_radius)
    .extrude(wall)
)

if __name__ == '__main__':
    exporters.export(solar_module_case, './exports/solar_module_case.stl')