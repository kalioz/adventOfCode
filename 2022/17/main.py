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


ROCKS_STR="""####

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
##"""

ROCKS = ROCKS_STR.split('\n\n')

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
        self.min_y=0 # min_x represent the value grid[0] represents. used when trying to find big number iterations.

        self.adapt_height(height)


    def adapt_height(self, height=3):
        height-=self.min_y
        for _ in range(height - len(self.grid)):
            self.grid.append([" "] * self.max_width)
    
    def get_current_max_height(self) -> int:
        """return the height at which any object (@ / #) is detected"""
        for height in range(len(self.grid)-1, -1, -1):
            if "#" in self.grid[height]:
                return height+1+self.min_y
        return 0
    
    def can_be_moved(self, rock: Rock, x: int, y: int) -> bool:
        """
        Check if a rock object can be moved.
        The rock is a string representing the rock, with "#" indicating where the rock is. the string can contain multiple lines.
        x,y represent the leftmost bottom point of the structure. it can represent an empty space if it is defined as such.

        returns True if there isn't already taken space in the place.
        """
        y-=self.min_y

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

        y-=self.min_y

        for point in rock.components:
            self.grid[y+point.y][x+point.x] = symbol
    
    def count_blocks(self, y, yy):
        """
            count the number of blocks '#' between the y and the y+yy lines.
        """
        return sum([
            line.count('#')
            for line in self.grid[y:y+yy]
        ])

    
    def find_recurring_pattern(self) -> int:
        """
            Check if a reccuring pattern is found

            a recurring pattern will have the following structure :
            - first k lines are unique due to the ground at y=0
            - then next lines are repeated every x line

            meaning the total height of the structure is = k + n * x 

            If found, return the value for (k, x)
            else returns None
        """

        repr = self.__repr__()

        number_lines_checked = 300 # number of lines we'll try to find a repeat of; higher is better as it will remove wrong leads from the results.
        starting_delta_line_checked=10000 # must be high enough to prevent unfinished lines fucking up the recognition

        if len(repr) < (2+1+self.max_width) * (number_lines_checked + starting_delta_line_checked):
            return None

        first_lines = repr[-(2+1+self.max_width) * (number_lines_checked + starting_delta_line_checked):-(2+1+self.max_width) * (starting_delta_line_checked)] # (2: side "|", 1: "\n") - currently check if we can find the last 300 lines repeated; skip 300 lines to be sure we don't have any line not yet completed.
        x_line=len(first_lines)//2 # cut the processing time by 2
        while True:
            try:
                x_line = repr.index(first_lines, x_line+1) # TODO warn: if the 300 lines can appear out of the blue, they WILL fuck up the x_line_next - x_line
                x_line_next = repr.index(first_lines, x_line+1)
            except ValueError:
                # no more first line found in the later stages
                return None

            x_repeat = int((x_line_next-x_line) / (2+1+self.max_width))

            if self.grid[10*x_repeat:11 * x_repeat] == self.grid[11*x_repeat:12*x_repeat] == self.grid[12*x_repeat:13*x_repeat]:
                # pattern found
                pattern = repr[x_line:x_line_next]
                k_repr = repr.index(pattern)
                k = int(k_repr / (2+1+self.max_width)) - 1
                return k, x_repeat

    def __repr__(self) -> str:
        output=[]
        output.append("."+"-"*self.max_width+".\n")
        for line in self.grid:
            output.append("|"+ "".join(line) +"|\n")
        return "".join(output[::-1])

def solve(jet_pattern: str, number_of_rocks=1_000_000_000_000):
    """
        jet_pattern: ">>><<><<><>" : indicates the direction the rocks are pushed at each turn.
    """
    grid = Grid()

    time_i = 0

    possible_recurring_pattern_ratio = 10_000 # arbitrary number set to check if we find a pattern every k rocks placed.

    rock_i = 0
    while rock_i < number_of_rocks:
        current_rock = ROCKS[rock_i%len(ROCKS)]

        current_height = grid.get_current_max_height()
        new_max_height = current_height + 3 + current_rock.height

        grid.adapt_height(new_max_height)

        x = 2
        y = current_height + 3

        while True:
            # lateral movement
            if jet_pattern[time_i%len(jet_pattern)] == ">":
                if grid.can_be_moved(current_rock, x + 1, y):
                    x=x+1
            elif grid.can_be_moved(current_rock, x - 1, y):
                x=x-1

            time_i+=1

            # down movement
            if grid.can_be_moved(current_rock, x, y-1):
                y-=1
            else:
                # rock can't fall down anymore: place it.
                grid.place(current_rock, x, y)
                break
        
        if rock_i > 0 and rock_i % possible_recurring_pattern_ratio == 0:
            # check recurring patterns to speed up time
            pattern_x = grid.find_recurring_pattern()
            if pattern_x is not None:
                first_k_non_repeated_lines, repeat_line_every = pattern_x
                # find out how much blocks are needed to fill one of the repetitions
                # assume every rock is placed the same number of times
                total_points_rocks = ROCKS_STR.count("#")
                total_points_repeated = grid.count_blocks(first_k_non_repeated_lines+1, repeat_line_every)

                number_rocks_repeated = len(ROCKS) * total_points_repeated // total_points_rocks
                
                # skip the long wait and go straight to the end
                new_rock_i = next(
                    number_of_rocks - number_rocks_repeated - i for i in range(number_rocks_repeated)
                    if (number_of_rocks - number_rocks_repeated - i - rock_i) % number_rocks_repeated == 0
                )
                diff_rock_i = new_rock_i - rock_i
                grid.min_y = (diff_rock_i // number_rocks_repeated) * repeat_line_every
                rock_i = new_rock_i

                
        rock_i+=1

    return grid.get_current_max_height()

# check that test data works
out1 = solve(test_data, 2022)

if out1 != 3068:
    print(f"test : {out1} != 3068")
    raise Exception("Bad result on test data")

out2 = solve(test_data, 1_000_000_000_000)
if out2 != 1_514_285_714_288:
    print(f"test : {out2} != 1_514_285_714_288")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve(data, 2022)}") 

print(f"result 2: {solve(data, 1_000_000_000_000)}")