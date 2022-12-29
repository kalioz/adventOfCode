import os, math, time, re, copy

from collections.abc import Iterator

from dataclasses import dataclass

from multiprocessing import Pool, SimpleQueue, cpu_count
from functools import partial
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./test_data"), 'r') as fi:
    test_data = "".join(fi.readlines())
    test_data = test_data.splitlines()

with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.splitlines()

@dataclass
class Point:
    x: int
    y: int
    z: int

    adjacent_points: set["Point"]

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.adjacent_points = set()

    def toTuple(self):
        return (self.x, self.y, self.z)

    def distanceTo(self, p: "Point") -> int:
        return math.dist(self.toTuple(), p.toTuple())
    
    def __hash__(self) -> int:
        return hash(self.toTuple())
    
    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y and self.z == o.z

@dataclass
class Droplet:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points

        self.minPoint = Point(
            x= min(p.x for p in points),
            y= min(p.y for p in points),
            z= min(p.z for p in points),
        )

        self.maxPoint = Point(
            x= max(p.x for p in points),
            y= max(p.y for p in points),
            z= max(p.z for p in points),
        )

        # set of points guaranteed to be outside
        self.__outside_points : set[Point] = set()

        # set of points guaranteed to be inside
        self.__inside_points : set[Point] = set()

    def get_neighbours(self, point: Point, exclude_droplet = True) -> Iterator[Point]:
        for x,y,z in [(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)]:
            adjacent_point = Point(x=point.x+x,y=point.y+y,z=point.z+z)
            if adjacent_point in self.points:
                if not exclude_droplet:
                    yield self.points[self.points.index(adjacent_point)]
            else:
                yield adjacent_point

    def is_air_trapped(self, p: Point):
        """Check if a bubble of air is exposed to the exterior or not."""
        current_search = set([p])
        already_passed = set([p])

        while len(current_search) > 0:
            next_search = set()
            for point in current_search:
                for adjacent_point in self.get_neighbours(point):
                    if adjacent_point in already_passed:
                        continue
                    if adjacent_point in self.points:
                        continue

                    already_passed.add(adjacent_point)
                    if adjacent_point in self.__outside_points:
                        self.__outside_points.add(p)
                        return False
                    if adjacent_point in self.__inside_points:
                        self.__inside_points.add(p)
                        return True

                    if ( 
                        not (self.maxPoint.x >= adjacent_point.x >= self.minPoint.x) or 
                        not (self.maxPoint.y >= adjacent_point.y >= self.minPoint.y) or 
                        not (self.maxPoint.z >= adjacent_point.z >= self.minPoint.z)
                    ):
                        # outside boundaries
                        self.__outside_points.add(p)
                        return False

                    next_search.add(adjacent_point)
            current_search = next_search
        self.__inside_points.add(p)
        return True
    
    def calculate_exterior_superficy(self):
        """calculate the number of surfaces exposed to the exterior"""
        output=0
        for point in self.points:
            for adjacent_surface_point in self.get_neighbours(point):
                if not self.is_air_trapped(adjacent_surface_point):
                    output+=1
        return output

def parse(d):
    output: list[Point] = []
    for line in d:
        x,y,z = eval(line)
        output.append(Point(x=x, y=y, z=z))
    
    # calculate adjacent points
    for p1 in range(len(output)):
        for p2 in range(p1+1, len(output)):
            if output[p1].distanceTo(output[p2]) == 1:
                output[p1].adjacent_points.add(output[p2])
                output[p2].adjacent_points.add(output[p1])

    return Droplet(points = output)

def solve_1(data):
    droplet = parse(data)
    return sum([
        6 - len(point.adjacent_points)
        for point in droplet.points
    ])

def solve_2(data):
    droplet = parse(data)

    return droplet.calculate_exterior_superficy()

# check that test data works
out1 = solve_1(test_data)

if out1 != 64:
    print(f"test : {out1} != 64")
    raise Exception("Bad result on test data")

out2 = solve_2(test_data)
if out2 != 58:
    print(f"test : {out2} != 58")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 

print(f"result 2: {solve_2(data)}")