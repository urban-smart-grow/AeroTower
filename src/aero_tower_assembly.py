from cadquery import Assembly, Color, Location, Vector, exporters
from tank import tank, socket_height as tank_socket_h
from tank_adapter import tank_adapter
from body import body, socket_height as body_socket_h, socket_offset
from plant_cup import plant_cup
from head_mount import head_mount, wall as head_mount_wall
from head_electronics_case import head_electronics_case
from head_electronics_lid import lid as head_electronics_lid
from head_tank import head_tank as head_tank
from utils.calculate_points_on_circle import calculate_circle_points

assembly = Assembly()

assembly.add(tank)

assembly.add(tank_adapter, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen-tank_socket_h
)))

assembly.add(body, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen-tank_socket_h
)))

for x, y in calculate_circle_points(5, socket_offset):
    assembly.add(
        plant_cup,
        loc=Location(
            Vector(x, y,
                   tank.BoundingBox().zlen
                   - tank_socket_h
                   + body.combine().objects[0].BoundingBox().zlen/2
                   ),
            Vector(-y, x, 0),
            45
        )
    )

assembly.add(head_mount, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen
    - tank_socket_h
    + body.combine().objects[0].BoundingBox().zlen
    - body_socket_h
)))

assembly.add(head_tank, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen
    - tank_socket_h
    + body.combine().objects[0].BoundingBox().zlen
    - body_socket_h
    + head_mount.combine().objects[0].BoundingBox().zlen
    - head_mount_wall/2
    - head_tank.combine().objects[0].BoundingBox().zlen/2
)))

assembly.add(head_electronics_case, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen
    - tank_socket_h
    + body.combine().objects[0].BoundingBox().zlen
    - body_socket_h
    + head_mount.combine().objects[0].BoundingBox().zlen
    - head_mount_wall
)))

assembly.add(head_electronics_lid, loc=Location(Vector(
    0, 0,
    tank.BoundingBox().zlen
    - tank_socket_h
    + body.combine().objects[0].BoundingBox().zlen
    - body_socket_h
    + head_mount.combine().objects[0].BoundingBox().zlen
    - head_mount_wall
    + head_electronics_lid.combine().objects[0].BoundingBox().zlen
), Vector(0, 1, 0), 180))


if __name__ == '__main__':
    exporters.export(assembly.toCompound(), './exports/assembly.stl')
