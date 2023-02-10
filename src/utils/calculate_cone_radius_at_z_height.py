def calculate_cone_radius_at_z_height(bottom_r, top_r, cone_height, z):
    if (bottom_r == top_r):
        return bottom_r
    if (bottom_r < top_r):
        return bottom_r + (top_r-bottom_r) * (z/cone_height)
    if (bottom_r > top_r):
        return bottom_r - (bottom_r-top_r) * (z/cone_height)
