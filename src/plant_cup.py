import cadquery as cq
import math
from primitives.cone import cone

height = 80
bottom_diameter = 52
top_diameter = 60
wall_strength = 2
hole_d = 6

offsets = range(0, bottom_diameter//2, 10)
radians = [math.radians(deg) for deg in range(0, 360, 40)]
points = [(math.cos(rad)*offset, math.sin(rad)*offset)
          for rad in radians for offset in offsets]


plant_cup = (
    cone(
        top_diameter,
        bottom_diameter,
        height
    )
    .pushPoints(points)
    .hole(hole_d)
    - cone(
        top_diameter-wall_strength,
        bottom_diameter-wall_strength,
        height-wall_strength,
    ).translate((0, 0, wall_strength))
)

if __name__ == '__main__':
    cq.exporters.export(plant_cup, './exports/plant_cup.stl', )
