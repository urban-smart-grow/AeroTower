import cadquery as cq
import math
from primitives.hollow_cone import hollow_cone

height = 80
bottom_diameter = 52
top_diameter = 60
wall_strength = 1
hole_d = 6

offsets = range(0, bottom_diameter//2, 10)
radians = [math.radians(deg) for deg in range(0, 360, 40)]
points = [(math.cos(rad)*offset, math.sin(rad)*offset)
          for rad in radians for offset in offsets]


cq.Workplane.hollow_cone = hollow_cone

plant_cup = (
    cq.Workplane('XY')
    .hollow_cone(
        top_diameter,
        bottom_diameter,
        height,
        wall_strength
    )
    .workplane()
    .pushPoints(points)
    .hole(hole_d)
    .combine()
)

if __name__ == '__main__':
    cq.exporters.export(plant_cup, './exports/plant_cup.stl', )
