from solid2 import cylinder, translate, difference
from subprocess import run

from solid2.core import difference


def ring(r=10, r1=None, r2=None, d1=None, d2=None, h=2, w=2, dx=0, dy=0, dz=0, center=False):
    """a cylinder with a hole

    Args:
        r (float, optional): outer radius. Defaults to 10.
        r1 (float, optional): outer, bottom radius. Defaults to None.
        r2 (float, optional): outer, top radius. Defaults to None.
        d1 (float, optional): outer, bottom diameter. Defaults to None.
        d2 (float, optional): outer, top diameter. Defaults to None.
        h (float, optional): height. Defaults to 2.
        w (float, optional): wall thickness. Defaults to 2.
        center (bool, optional): wether the ring is centered. Defaults to False.

    Returns:
        OpenSCADObject: a cylinder with a hole
    """
    if d1 is not None:
        r1 = d1/2
    if d2 is not None:
        r2 = d2/2

    r1 = r1 or r
    r2 = r2 or r1

    outer = cylinder(r1=r1, r2=r2, h=h, center=center)
    inner = cylinder(r1=r1-w, r2=r2-w, h=h, center=center)
    ring = difference()(outer, inner)

    return ring


if __name__ == '__main__':
    ring().save_as_stl('ring.stl')
    run(['code', 'open', 'ring.stl'])
