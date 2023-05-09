from cadquery import cq, exporters
import head_electronics_lid
# import body
import math

wall = 1
body_overlap = 4
gap = 0.4
body_diameter = 160  # body.diameter
body_radius = body_diameter / 2
outer_radius = body_radius + wall
inner_radius = body_radius + gap
cable_hole_radius = 8
lid_bounding_box = head_electronics_lid.lid.combine().objects[0].BoundingBox()

electronics_case_outstand = math.ceil(
    head_electronics_lid.lid.combine().objects[0].BoundingBox().zlen
    + wall
)
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
    .circle(cable_hole_radius)
    .extrude(wall)
)

center_of_outline = (
    (lid_bounding_box.ylen/2 +
     inner_radius) / 2
)

# battery clamp

battery_xlen = 50
battery_ylen = 6
battery_zlen = 30
clamp_wall = 1.2

battery_clamp_y_offset = center_of_outline

solar_module_case = (
    solar_module_case
    .workplaneFromTagged('base')
    .move(0, battery_clamp_y_offset)
    .rect(battery_xlen+clamp_wall*2, battery_ylen+clamp_wall*2)
    .rect(battery_xlen, battery_ylen)
    .extrude(battery_zlen)
)

# board clamp

board_xlen = 8
board_ylen = 40
board_zlen = 20
clamp_wall = 1.2

board_clamp_y_offset = (
    lid_bounding_box.ylen
    - board_ylen
) / 2

board_clamp_x_offset = center_of_outline - board_xlen - wall

solar_module_case = (
    solar_module_case
    .workplaneFromTagged('base')
    .move(board_clamp_x_offset, board_clamp_y_offset)
    .rect(board_xlen+clamp_wall*2, board_ylen+0.1)
    .rect(board_xlen, board_ylen)
    .extrude(board_zlen)
)

if __name__ == '__main__':
    exporters.export(solar_module_case, './exports/solar_module_case.stl')
