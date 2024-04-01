import math

# Helper functions for the helper functions
def norm(v):
    return math.sqrt(v[0]**2, v[1]**2)
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
def dot(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]
def intersection_point(p1, p2, q1, q2):
    # Calculate slopes of the lines
    slope_p = (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] != p1[0] else float('inf')
    slope_q = (q2[1] - q1[1]) / (q2[0] - q1[0]) if q2[0] != q1[0] else float('inf')

    # If slopes are the same, lines are parallel
    if slope_p == slope_q:
        return None

    # If one of the slopes is infinity (vertical line)
    if slope_p == float('inf'):
        x = p1[0]
        y = slope_q * (x - q1[0]) + q1[1]
    elif slope_q == float('inf'):
        x = q1[0]
        y = slope_p * (x - p1[0]) + p1[1]
    else:
        # Calculate intersection point
        x = ((q1[1] - p1[1]) + slope_p * p1[0] - slope_q * q1[0]) / (slope_p - slope_q)
        y = slope_p * (x - p1[0]) + p1[1]

    return (x, y)
def angle_between_vectors(a, b):
    dot = dot(a, b)
    magnitude_a = norm(a)
    magnitude_b = norm(b)

    if magnitude_a == 0 or magnitude_b == 0:
        return None

    cos_angle = dot / (magnitude_a * magnitude_b)
    angle = math.acos(cos_angle)
    return angle


# NOTE: These functions have no bounds checking.
# Check if your returned values are within range (e.g. steer between -1 and 1)

# Gives a steer that travels along a circle with specific radius.
def radius_to_steer(radius: float, min_turn: float):
    return radius/min_turn

# Gives the radius of turning circle given a steer.
def steer_to_radius(steer: float, min_turn: float):
    return steer*min_turn

# Gives a steer that changes final degree by the given angle.
def degree_to_steer(change_in_angle: float, speed: float, min_turn: float):
    return radius_to_steer(speed/math.radians(change_in_angle), min_turn)

# Gives offset of a plane with given characteristics at turn t.
def get_path_offset(t: float, steer: float, init_angle: float, speed: float, min_turn: float):
    radius = steer_to_radius(steer, min_turn)
    init_angle_rad = math.radians(init_angle)-math.pi*3/2
    x = math.cos(t*(speed/radius)+init_angle_rad)
    y = math.sin(t*(speed/radius)+init_angle_rad)

    x -= math.cos(init_angle_rad)
    y -= math.sin(init_angle_rad)

    return (x*radius, y*radius)

# Gives (steer, num_turns) for a plane to pass through a given offset point. 
def point_to_steer(x: float, y: float, init_angle: float, min_turn: float, speed: float):
    rad = math.radians(init_angle)
    cent_vec = [math.cos(rad+math.pi/2), math.sin(rad+math.pi/2)]
    #finds perpendicular vector to the line from starting point (0,0) to offset
    other_vec_start = [x/2, y/2]
    other_vec_end = [-y + x/2, x + y/2]
    cent = intersection_point([0,0], cent_vec, other_vec_start, other_vec_end)
    if cent==None:
        return (0, norm([x,y])/speed)
    else:
        return (radius_to_steer(norm(cent), min_turn), angle_between_vectors(cent_vec, [-y, x])*norm(cent)/speed)

    
