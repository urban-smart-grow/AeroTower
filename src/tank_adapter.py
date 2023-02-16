from cadquery import Vector, cq, exporters
from cq_warehouse.thread import IsoThread
from constants import thread_gap_in_mm
import tank
import body

outer_thread = IsoThread(
    major_diameter=tank.diameter-(tank.wall*2)-(thread_gap_in_mm*2),
    external=True,
    length=tank.socket_height,
    pitch=tank.pitch,
    end_finishes=('fade', 'fade')
)

inner_thread = IsoThread(
    major_diameter=body.bottom_thread_major_diameter,
    external=False,
    length=body.socket_height,
    pitch=body.pitch,
    end_finishes=('fade', 'fade')
)

tank_adapter = (
    cq.Workplane('XY')
    .circle(outer_thread.min_radius)
    .circle(body.bottom_thread_major_diameter/2)
    .extrude(body.socket_height)
    .add(outer_thread.Solids())
    .add(inner_thread.Solids())
)

if __name__ == '__main__':
    exporters.export(tank_adapter, './exports/tank_adapter.stl')
