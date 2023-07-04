from cadquery import cq, exporters
from utils.calculate_points_on_circle import calculate_circle_points
import plant_cup

height = 2
vent_d = 1.4

level_height = height/2
top_r = plant_cup.top_diameter/2-plant_cup.wall_strength
pitch = ((plant_cup.top_diameter-plant_cup.bottom_diameter)/2)/plant_cup.height
bottom_r = top_r-pitch*level_height

plant_cup_lid = (
    cq.Workplane('XY')
    .cylinder(
        level_height,
        plant_cup.top_diameter/2,
        centered=(True, True, False)
    )
    .add(
        cq.Solid
        .makeCone(top_r, bottom_r, level_height)
        .translate((0, 0, level_height))
    )
    .faces('<Z')
    .workplane()
    .pushPoints(
         list(calculate_circle_points(3, top_r*0.11))
        + list(calculate_circle_points(5, top_r*0.33))
        + list(calculate_circle_points(9, top_r*0.66))
    )
    .hole(vent_d, height)
)

if __name__ == '__main__':
    exporters.export(plant_cup_lid, './exports/plant_cup_lid.stl')
