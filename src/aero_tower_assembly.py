from cadquery import Assembly, Color, Location, Vector, exporters
from tank import tank, socket_height as tank_socket_h
from tank_adapter import tank_adapter
from body import body, cup_bottom_overhang_in_mm, socket_height as body_socket_h, socket_offset
from plant_cup import plant_cup, height as cup_height
from head_mount import head_mount, wall as head_mount_wall
from head_electronics_case import head_electronics_case
from head_electronics_lid import lid as head_electronics_lid
from head_tank import head_tank as head_tank
from utils.calculate_points_on_circle import calculate_circle_points


def make_assembly(explosion_factor=1):
    assembly = Assembly()
    assembly.add(tank)

    tank_adapter_vector = Vector(
        0, 0,
        tank.BoundingBox().zlen-tank_socket_h
    )

    tank_adapter_explosion_factor = (explosion_factor-1)/2 + \
        1 if explosion_factor != 1 else 1

    head_explosion_factor = (explosion_factor-1)*1.3 + 1 \
        if explosion_factor != 1 else 1

    assembly.add(tank_adapter, loc=Location(
        tank_adapter_vector*tank_adapter_explosion_factor))

    assembly.add(body, loc=Location(tank_adapter_vector * explosion_factor))

    for x, y in calculate_circle_points(5, socket_offset):
        plant_cup_vector = (
            Vector(x, y,
                   tank.BoundingBox().zlen
                   - tank_socket_h
                   - cup_bottom_overhang_in_mm
                   - (cup_height * 0.01)
                   + body.combine().objects[0].BoundingBox().zlen/2
                   )
        )

        assembly.add(
            plant_cup,
            loc=Location(
                plant_cup_vector * explosion_factor,
                Vector(-y, x, 0),
                45
            )
        )

    head_mount_vector = Vector(
        0, 0,
        tank.BoundingBox().zlen
        - tank_socket_h
        + body.combine().objects[0].BoundingBox().zlen
        - body_socket_h
    )

    assembly.add(head_mount, loc=Location(
        head_mount_vector * explosion_factor))

    head_tank_vector = Vector(
        0, -8,
        tank.BoundingBox().zlen
        - 6
        - tank_socket_h
        + body.combine().objects[0].BoundingBox().zlen
        - body_socket_h
        + head_mount.combine().objects[0].BoundingBox().zlen
        - head_mount_wall/2
        - head_tank.combine().objects[0].BoundingBox().zlen/2
    )

    assembly.add(head_tank, loc=Location(
        head_tank_vector * head_explosion_factor))

    case_vector = Vector(
        0, 12,
        tank.BoundingBox().zlen
        - 6
        - tank_socket_h
        + body.combine().objects[0].BoundingBox().zlen
        - body_socket_h
        + head_mount.combine().objects[0].BoundingBox().zlen
        - head_mount_wall
    )

    assembly.add((
        head_electronics_case
    ), loc=Location(
        case_vector * head_explosion_factor,
        Vector(0, 0, 1),
        90
    )
    )

    lid_vector = Vector(
        0, 0,
        tank.BoundingBox().zlen
        - tank_socket_h
        + body.combine().objects[0].BoundingBox().zlen
        - body_socket_h
        + head_mount.combine().objects[0].BoundingBox().zlen
        - head_mount_wall
        + head_electronics_lid.combine().objects[0].BoundingBox().zlen
    )

    assembly.add((
        head_electronics_lid
        .rotate(Vector(), (0, 0, 1), 90)),
        loc=Location(lid_vector * head_explosion_factor, Vector(0, 1, 0), 180))

    return assembly


assembly = make_assembly()
explosion = make_assembly(1.7)

if __name__ == '__main__':
    exporters.export(assembly.toCompound(), './exports/assembly.stl')
    exporters.export(explosion.toCompound(), './exports/explosion.stl')
