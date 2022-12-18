import os, math, time, re

from Point import Point

from multiprocessing import Pool, SimpleQueue
from functools import partial
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
        distance = sensor["beacon"].distance_manhattan(sensor["sensor"])
        intersections = calculate_intersections(sensor["sensor"], distance, y)
        if len(intersections) == 2:    
            points_x_cannot_have_beacon.update(range(intersections[0].x, intersections[1].x+1))
        elif len(intersections) == 1:
            points_x_cannot_have_beacon.add(intersections[0].x)
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

    for sensor in list_sensors:
        sensor["distance"] = sensor["sensor"].distance_manhattan(sensor["beacon"])

    with Pool() as pool:
        results = pool.imap_unordered(partial(solve_2_one_line, list_sensors=list_sensors, max_range=max_range), range(max_range))
  
        return next(value for value in results if value is not None)

    # for y in range(max_range):
        
    #     out=solve_2_one_line(y,list_sensors, max_range)
    #     if out is not None:
    #         return out

    return None

def solve_2_one_line(y,list_sensors, max_range):
    """Check if we can find a solution for the solution 2 on the line y
        Used for multiprocessing purposes
    """
    x=0
    while x <= max_range:
        # check if (x,y) is in one of the sensors
        for sensor in list_sensors:
            # if one of the sensor is in matching distance : go to the end of its range to speed things up
            if sensor["sensor"].distance_manhattan(x, y) <= sensor["distance"]:
                intersections = calculate_intersections(sensor["sensor"], sensor["distance"], y)
                x = intersections[-1].x
                break
        else:
            return x * 4000000 + y
        x+=1
    return 

if solve_1(test_data, 10) != 26:
    print(f"test : {solve_1(test_data, 10)} != 26")
    raise Exception("Bad result on test data")

if solve_2(test_data, 20) != 56000011:
    print(f"test : {solve_2(test_data, 20)} != 56000011")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 
# 5394083 too high
# 5733733
print(f"result 2: {solve_2(data)}") # 11583882601918