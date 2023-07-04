import cadquery as cq

cube = cq.Workplane('XY').box(10, 10, 10)

cq.exporters.export(cube, 'test.stl')
