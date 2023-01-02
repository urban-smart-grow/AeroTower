from cadquery import Location, Vector, Workplane, cq, exporters
from utils.calculate_points_on_circle import calculate_circle_points
import plant_cup

wall = 1
diameter = 160
height = 180


body = (
    cq.Workplane('XY')
    .circle(diameter/2)
    .circle(diameter/2-wall)
    .extrude(height)
    .workplane()
    .pushPoints(calculate_circle_points(5, 80))
    .cutEach(
        lambda loc:
        cq.Solid.makeCone(
            plant_cup.bottom_diameter/2,
            plant_cup.top_diameter/2,
            plant_cup.height
        ).rotate(Vector(0, 0, 0), Vector(1, 1, 0), 45)
        .locate(loc)
    )

)
exporters.export(body, './exports/body.stl')
