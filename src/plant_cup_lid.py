from cadquery import cq, exporters
from utils.calculate_points_on_circle import calculate_circle_points
import plant_cup

base_h = 0.5
skirt_h = 3
vent_d = 1.4

base_r = plant_cup.top_diameter/2
skirt_r = base_r+plant_cup.wall_strength

plant_cup_lid = (
    cq.Workplane('XY')
    .tag('base')
    .cylinder(
        base_h,
        base_r,
    )
    .faces('<Z')
    .workplane()
    .pushPoints(
        list(calculate_circle_points(3, base_r*0.11))
        + list(calculate_circle_points(5, base_r*0.33))
        + list(calculate_circle_points(9, base_r*0.66))
    )
    .hole(vent_d, base_h)
    .workplaneFromTagged('base')
    .circle(skirt_r)
    .circle(base_r)
    .extrude(skirt_h)
)

if __name__ == '__main__':
    exporters.export(plant_cup_lid, './exports/plant_cup_lid.stl')
