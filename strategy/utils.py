import math
from game.plane import Plane

# Helper functions for the helper functions
# These assume the vector is length two, and will essentially truncate longer vectors
def norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
def dot(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]
def neg(v):
    return [-v[0], -v[1]]
def add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]
def mul(s, v):
    return [s*v[0], s*v[1]]

def intersection_point(p1, p2, q1, q2):
    """
    Returns the intersection of two lines, one of which goes through points p1 and p2,
    and the other of which goes through points q1 and q2. Points are given as tuples or lists with length two.

    Returns None if the lines are parallel.
    """

    # Calculate slopes of the lines
    slope_p = (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] != p1[0] else float('inf')
    slope_q = (q2[1] - q1[1]) / (q2[0] - q1[0]) if q2[0] != q1[0] else float('inf')

    # If slopes are the same, lines are parallel
    if slope_p == slope_q:
        # print("AAAA")
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
    """
    Returns the angle between two vectors a, b.
    
    Vectors are in the form of a list or tuple with length two.
    """
    dot_prod = dot(a, b)
    magnitude_a = norm(a)
    magnitude_b = norm(b)

    if magnitude_a <.0001 or magnitude_b < .0001:
        return None

    cos_angle = max(1, dot_prod / (magnitude_a * magnitude_b))
    angle = math.acos(cos_angle)
    return angle


# NOTE: These functions have no bounds checking.
# Check if your returned values are within range (e.g. steer between -1 and 1)

# NOTE: Every angle input and output is in DEGREES.

def radius_to_steer(radius: float, min_turn: float):
    """Returns a steer that travels along a circle with specific radius."""
    return min_turn/radius

def steer_to_radius(steer: float, min_turn: float):
    """Gives the radius of turning circle given a steer."""
    return steer*min_turn

def degree_to_steer(change_in_angle: float, speed: float, min_turn: float):
    """Gives a steer that changes final degree by the given angle."""
    return radius_to_steer(speed/math.radians(change_in_angle), min_turn)

def degree_to_radius(degree: float, speed: float):
    """Given a change of degree, returns corresponding radius of the turning circle"""
    return speed/math.radians(degree)

def radius_to_degree(radius: float, speed: float):
    """Given a radius of a turning circle, returns the degrees changed per turn"""
    return math.degrees(speed/radius)

def get_path_offset(t: float, steer: float, init_angle: float, speed: float, min_turn: float):
    """
    Returns the OFFSET of a plane with a given steer and at a given turn

    Parameters:
        t (float): The queried turn. t can be any real number (e.g, t=.05 means after half a turn)
        steer (float): The given steer, which is assumed to be constant.
        init_angle (float): The inital facing of a given plane.
        speed (float): The current speed of a given plane.
        min_turn (float): The smallest turning circle this plane can achieve

    Returns:
    (x, y, angle): The (x,y) represents the positional OFFSET from the inital position, and (angle)
        gives the CHANGE in angle
    """
    radius = steer_to_radius(steer, min_turn)
    init_angle_rad = math.radians(init_angle)

    # init angle is the direction the plane faces, so we need to shift to get the angle where the plane
    # is on the turning circle
    if (steer == 0):
        return (speed * math.cos(init_angle_rad), speed * math.sin(init_angle_rad), init_angle)
    elif (steer < 0):
        init_angle_rad += math.pi / 2
    else:
        init_angle_rad -= math.pi / 2

    # Start with the vector from the center of the unit turning circle to the final position
    x = math.cos(t*(speed/radius)+init_angle_rad)
    y = math.sin(t*(speed/radius)+init_angle_rad)

    # Subtract the vector from the plane's actual position to the center of the unit turning circle
    x -= math.cos(init_angle_rad)
    y -= math.sin(init_angle_rad)

    # Scale the final offset by the radius of the turning circle.
    return (x*abs(radius), y*abs(radius), math.degrees(t*speed/radius))

def plane_path_offset(t: float, steer: float, plane: Plane):
    """
    Returns the ABSOLUTE location and angle of a plane with a given steer and at a given turn

    Parameters:
        t (float): The queried turn. t can be any real number (e.g, t=.05 means after half a turn)
        steer (float): The given steer, which is assumed to be constant.
        plane (Plane): The queried plane.

    Returns:
    (x, y, angle): The (x,y) represents the actual position of the plane after t turns, and (angle)
        gives the actual angle.
    """
    turn_radius = degree_to_radius(plane.stats.turn_speed, plane.stats.speed)
    off = get_path_offset(t, steer, plane.angle, plane.stats.speed, turn_radius)
    return (plane.position.x + off[0], plane.position.y + off[1], plane.angle + off[2])

def fly_to_offset(x: float, y: float, init_angle: float, min_turn: float, speed: float):
    """
    Two points and a tangent line uniquely defines a circle. Thus, this function returns the
    the steer needed to travel along said circle, as well as the number of turns to reach
    the desired point.

    NOTE: This function gives especially poor steers when the given offset is "behind" the plane,
    since this function will then try to travel around the circle the long way.

    Parameters:
        x (float): The OFFSET x to fly towards.
        y (float): The OFFSET y to fly towards.
        init_angle (float): The angle of the plane in degrees.
        min_turn (float): The smallest turning circle this plane can achieve.
        speed (float): The speed of the plane.
    
    Returns:
        (steer, turns): The steer required for a plane to pass through a given OFFSET point after (turns) turns"""
    
    # this function finds the center of the unique circle by finding the intersection between
    # the line perpendicular to the facing of the plane, and the line of points equidistant to
    # the start and end point (perpendicular bisector)
    if (x == 0 and y == 0):
        return (0,0)
    rad = math.radians(init_angle)
    heading_perp_vec = [math.cos(rad+math.pi/2), math.sin(rad+math.pi/2)]
    other_vec_start = [x/2, y/2]
    other_vec_end = [-y + x/2, x + y/2]
    center = intersection_point([0,0], heading_perp_vec, other_vec_start, other_vec_end)
    
    if center==None:
        return (0, norm([x,y])/speed)
    radius = norm(center)
    if dot(heading_perp_vec, center) < 0:
        radius = -radius

    return (radius_to_steer(radius, min_turn), angle_between_vectors(neg(center), add(neg(center), [x, y]))*abs(radius)/speed)

def plane_find_path_to_point(x: float, y: float, plane: Plane):
    """
    Wrapper around fly_to_offset for a plane.
    Gives (steer, num_turns) for a plane to pass through a given ABSOLUTE point.

    Parameters:
        x (float): The ABSOLUTE x to fly towards.
        y (float): The ABSOLUTE y to fly towards.
        plane (Plane): A plane object with stats and a position
    
    Returns:
        (steer, turns): The steer required for a plane to pass through a given ABSOLUTE point after (turns) turns
    """
    xoff = x - plane.position.x
    yoff = y - plane.position.y
    turn_radius = degree_to_radius(plane.stats.turn_speed, plane.stats.speed)
    return fly_to_offset(xoff, yoff, plane.angle, turn_radius, plane.stats.speed)

def unavoidable_crash(x: float, y: float, angle: float, min_turn: float, lb = -50, rb = 50, db = -50, ub = 50):
    """
    Returns true if a plane at a given point and angle cannot avoid flying out of the given bounds

    NOTE: This function returns a false positive if the plane is close to the boundary but flying away.
    This is normally impossible to achieve assuming speed, turn rate, and boundary locations are constant.

    Parameters:
        x (float): x coord of the plane.
        y (float): y coord of the plane.
        angle (float): angle of the plane in degrees
        min_turn (float): the radius of the turning circle of the sharpest turn a plane can make
    
    Returns:
        Returns True if plane in position cannot avoid flying out of bounds.
        Returns False otherwise.
    """
    if (x < lb or x > rb or y < db or y > ub):
        return True
    rad = math.radians(angle)

    # Finds the centers of the smallest turning circles possible
    perp_vec = [math.cos(rad + math.pi/2), math.sin(rad + math.pi/2)]
    lvec = add([x, y], mul(min_turn, perp_vec))
    rvec = add([x, y], mul(-min_turn, perp_vec))

    # Checks if any point in either circle is out of bounds
    lob = False
    rob = False
    if lvec[0] + min_turn > rb or lvec[0] - min_turn < lb or lvec[1] + min_turn > ub or lvec[1] - min_turn < db:
        lob = True
    if rvec[0] + min_turn > rb or rvec[0] - min_turn < lb or rvec[1] + min_turn > ub or rvec[1] - min_turn < db:
        rob = True
    
    # If both left and right turns are out of bounds, the plane cannot avoid crashing.
    #
    # Alternatively, it might be close to a boundary but flying away. Note this situation
    # is not possible generally, since this would imply the plane was briefly out of bounds
    # in a previous turn
    if rob and lob:
        return True
    return False

def steer_crashes_plane(steer: float, plane: Plane):
    """
    Wrapper around unavoidable_crash.

    Returns True if a plane flying with the given steer will not be able to avoid crashing
    after flying one turn with the given steer. Returns False otherwise.

    NOTE: This function returns a false positive if the plane is close to the boundary but flying away.
    This is normally impossible to achieve assuming speed, turn rate, and boundary locations are constant.

    Parameters:
        steer (float): The given steer of a plane.
        plane (Plane): A queried plane.
    
    Returns:
        Returns True if plane in the given position will be unable to avoid a crash after
        one turn of flying at the given steer. Returns False otherwise.
    """
    turn_radius = degree_to_radius(plane.stats.turn_speed, plane.stats.speed)
    off = get_path_offset(1, steer, plane.angle, plane.stats.speed, turn_radius)
    position = add([plane.position.x,plane.position.y], off)
    return unavoidable_crash(position[0], position[1], off[2], turn_radius)