import os, math, time, re, copy

from dataclasses import dataclass

from multiprocessing import Pool, SimpleQueue, cpu_count
from functools import partial
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./test_data"), 'r') as fi:
    test_data = "".join(fi.readlines())

with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())


ROCKS="""####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split('\n\n')

@dataclass
class Point:
    x: int
    y: int

class Rock:
    def __init__(self, repr: str):
        self.repr = repr
        self.height = repr.count('\n') + 1
        self.components : list[Point] = [] # components are points relative to the leftmost bottom point; the leftmost bottom point can be absent from the components.

        for y, line in enumerate(repr.split('\n')):
            for x, item in enumerate(line):
                if item == "#":
                    self.components.append(Point(x = x, y=repr.count('\n')-y))
    

ROCKS = [Rock(rock) for rock in ROCKS]
DEBUG=False

class Grid:
    def __init__(self, max_width=7, height=3):
        self.max_width=7
        self.grid: list[list[str]]=[]

        self.adapt_height(height)
    
    def adapt_height(self, height=3):
        for _ in range(height - len(self.grid)):
            self.grid.append([" "] * self.max_width)
    
    def get_current_max_height(self) -> int:
        """return the height at which any object (@ / #) is detected"""
        for height in range(len(self.grid)-1, -1, -1):
            if "#" in self.grid[height]:
                return height+1
        return 0
    
    def can_be_moved(self, rock: Rock, x: int, y: int) -> bool:
        """
        Check if a rock object can be moved.
        The rock is a string representing the rock, with "#" indicating where the rock is. the string can contain multiple lines.
        x,y represent the leftmost bottom point of the structure. it can represent an empty space if it is defined as such.

        returns True if there isn't already taken space in the place.
        """

        for point in rock.components:
            if not (
                0 <= y + point.y < len(self.grid) and
                0 <= x + point.x < len(self.grid[y+point.y]) and
                self.grid[y+point.y][x+point.x] == " "
            ):
                return False
        return True
    
    def place(self, rock: Rock, x: int, y: int, symbol="#"):
        """
        Place a rock at the x,y position.
        """

        for point in rock.components:
            self.grid[y+point.y][x+point.x] = symbol
    
    def __repr__(self) -> str:
        output=[]
        output.append("."+"-"*self.max_width+".\n")
        for line in self.grid:
            output.append("|"+ "".join(line) +"|\n")
        return "".join(output[::-1])

def solve_1(jet_pattern: str, number_of_rocks=2022):
    """
        jet_pattern: ">>><<><<><>" : indicates the direction the rocks are pushed at each turn.
    """
    grid = Grid()

    time_i = 0

    for rock_i in range(number_of_rocks):
        current_rock = ROCKS[rock_i%len(ROCKS)]

        current_height = grid.get_current_max_height()
        new_max_height = current_height + 3 + current_rock.height

        grid.adapt_height(new_max_height)

        x = 2
        y = current_height + 3

        while True:
            if DEBUG:
                debug_grid = copy.deepcopy(grid)
                debug_grid.place(current_rock, x, y, symbol="@")
                print(debug_grid)

            # lateral movement
            if jet_pattern[time_i%len(jet_pattern)] == ">":
                if DEBUG:
                    print("push_right")
                if grid.can_be_moved(current_rock, x + 1, y):
                    x=x+1
            elif grid.can_be_moved(current_rock, x - 1, y):
                if DEBUG:
                    print("push_left")
                x=x-1

            time_i+=1

            # down movement
            if grid.can_be_moved(current_rock, x, y-1):
                y-=1
            else:
                # rock can't fall down anymore: place it.
                grid.place(current_rock, x, y)
                break
        if DEBUG:
            print(grid)

    return grid.get_current_max_height()

def solve_2(d, max_range=4000000):
    pass

# check that test data works
out1 = solve_1(test_data)

if out1 != 3068:
    print(f"test : {out1} != 3068")
    raise Exception("Bad result on test data")

# if solve_2(test_data, 20) != 56000011:
#     print(f"test : {solve_2(test_data, 20)} != 56000011")
#     raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 

# print(f"result 2: {solve_2(data)}") # 11583882601918