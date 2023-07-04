def calculate_circle_points(number_of_points: int, radius: float = 1):
    """calculate a given number of vertices placed 
    approximately evenly on a circle with a given radius

    Args:
        number_of_points (int)
        radius (float, optional): Defaults to 1.

    Returns:
        Generator of vertices
    """
    import math

    def make_convert(offset):
        return lambda map, angle: map(math.radians(angle))*offset

    convert = make_convert(radius)

    return (
        (convert(math.cos, angle), convert(math.sin, angle))
        for angle in range(0, 360, 360//number_of_points)
    )
