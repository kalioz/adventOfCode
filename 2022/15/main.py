import os, math, time, re

from Point import Point

dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./test_data"), 'r') as fi:
    test_data = "".join(fi.readlines())
    test_data = test_data.split('\n')

with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')


def parse(d):
    reg = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    output = []
    for line in d:
        m = reg.match(line)
        if m is None:
            raise Exception(f"Couldn't parse line : {line}")
        output.append({
            "sensor" : Point(int(m.group(1)), int(m.group(2))),
            "beacon" : Point(int(m.group(3)), int(m.group(4))),
        })

    return output

def calculate_intersections(p: Point, distance_manhattan: int, y: int) -> list[Point]:
    """Calculate intersection where calcul_distance_manhattan(p->output) == distance_manhattan, and output.y == y."""
    # check if it is atteignable
    if not (p.y-distance_manhattan <= y <= p.y+distance_manhattan):
        return []
    
    # if only one point would match
    if p.y-distance_manhattan == y or p.y+distance_manhattan == y:
        return [Point(p.x, y)]

    # then, two points would match
    return [
        Point(p.x - distance_manhattan + abs(p.y-y), y),
        Point(p.x + distance_manhattan - abs(p.y-y), y)
    ]

def get_positions_cannot_have_beacon(list_sensors, y, remove_existing_beacons=True) -> set[int]:
    points_x_cannot_have_beacon=set()
    # calculate minX and maxX that one of the detected beacon cannot be
    for sensor in list_sensors:
        t0=time.time()
        distance = sensor["beacon"].distance_manhattan(sensor["sensor"])
        t1=time.time()
        intersections = calculate_intersections(sensor["sensor"], distance, y)
        t2=time.time()
        if len(intersections) == 2:    
            points_x_cannot_have_beacon.update(range(intersections[0].x, intersections[1].x+1))
        elif len(intersections) == 1:
            points_x_cannot_have_beacon.add(intersections[0].x)
        t3=time.time()

        print("get_positions", t1-t0, t2-t1, t3-t2, len(intersections))

    # remove beacons from output
    if remove_existing_beacons:
        for sensor in list_sensors:
            if int(sensor["beacon"].y) == y and int(sensor["beacon"].x) in points_x_cannot_have_beacon:
                points_x_cannot_have_beacon.remove(sensor["beacon"].x)
        
    return points_x_cannot_have_beacon

def solve_1(d, y=2000000):
    # find all the positions where a beacon cannot be, specifically on the row index "y"
    list_sensors = parse(d)

    points_x_cannot_have_beacon=get_positions_cannot_have_beacon(list_sensors, y)

    return len(points_x_cannot_have_beacon)

def solve_2(d, max_range=4000000):
    list_sensors = parse(d)
    possible_x = set(range(max_range))
    for y in range(max_range):
        t0 = time.time()
        points_x_cannot_have_beacon=get_positions_cannot_have_beacon(list_sensors, y, remove_existing_beacons=False)

        t1 = time.time()
        found_x = possible_x - points_x_cannot_have_beacon
        t2 = time.time()
        if len(found_x) != 0:
            return found_x.pop() * 4000000 + y
        
        print(f"{y=} {t1-t0} {t2-t1}")

    return None

if solve_1(test_data, 10) != 26:
    print(f"test : {solve_1(test_data, 10)} != 26")
    raise Exception("Bad result on test data")

if solve_2(test_data, 20) != 56000011:
    print(f"test : {solve_2(test_data, 20)} != 56000011")
    raise Exception("Bad result on test data")


print(f"result 1: {solve_1(data)}") 
# 5394083 too high
# 5733733
print(f"result 2: {solve_2(data)}")