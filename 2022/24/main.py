import os, math, time, re, copy

from collections.abc import Iterator

from dataclasses import dataclass, field

import multiprocessing as mp
from multiprocessing.managers import SyncManager
from queue import PriorityQueue, Empty

dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./test_data"), 'r') as fi:
    test_data = "".join(fi.readlines())
    test_data = test_data.splitlines()

with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.splitlines()

DIRECTIONS={
    ">": (1,0),
    "<": (-1,0),
    "^": (0,-1),
    "v": (0,1)
}

@dataclass
class Blizzard:
    x: int
    y: int
    direction: tuple[int, int]

    def get_position_at_round(self, round: int, maxX: int, maxY: int):
        """
            return the position of the blizzard at the given round. 
        """
        return (
            (self.x + round * self.direction[0] - 1) % (maxX - 1) + 1,
            (self.y + round * self.direction[1] - 1) % (maxY - 1) + 1
            )

# TODO calculate when a case is empty at once (e.g. calculate every possibility there is of a blizzard), so that we end up with a simple formula to check if a case is viable

@dataclass
class GridPoint:

    def __init__(self, x:int, y:int, blizzards: list[Blizzard]) -> None:
        self.x = x
        self.y = y

        self.blizzards_affecting = [
            blizzard for blizzard in blizzards
            if (blizzard.x == x and blizzard.y == y)
            or (blizzard.x == x and blizzard.direction[0] == 0)
            or (blizzard.y == y and blizzard.direction[1] == 0)
        ]
    
    def is_under_blizzard(self, round: int, maxX: int, maxY: int):
        return any(
            blizzard.get_position_at_round(round, maxX=maxX, maxY=maxY) == (self.x, self.y)
            for blizzard in self.blizzards_affecting
        )
    
    def to_string(self, round: int, maxX: int, maxY: int) -> str:
        blizzards_in_effect = [
            blizzard
            for blizzard in self.blizzards_affecting
            if blizzard.get_position_at_round(round, maxX=maxX, maxY=maxY) == (self.x, self.y)
        ]
        if len(blizzards_in_effect) == 0:
            return "."
        elif len(blizzards_in_effect) == 1:
            return next(k for k, v in DIRECTIONS.items() if v == blizzards_in_effect[0].direction)
        else:
            return str(len(blizzards_in_effect))



class Grid:
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.blizzards: list[Blizzard] = []

        self.gridPoints: dict[tuple[int, int], GridPoint] = {}

        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                if char in DIRECTIONS:
                    self.blizzards.append(Blizzard(x=x, y=y, direction=DIRECTIONS[char]))

        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                self.gridPoints[(x, y)] = GridPoint(x, y, self.blizzards)
        
        self.startingPosition = (1,0)
        self.targetPosition = (len(grid[0])-2, len(grid)-1)

        self.maxPoint = (len(grid[0])-1, len(grid)-1)
    
    def is_position_in_blizzard(self, x: int, y: int, round: int) -> bool:
        """return true if the position is in a blizzard"""
        return self.gridPoints[(x,y)].is_under_blizzard(round=round, maxX = self.maxPoint[0], maxY=self.maxPoint[1])
    
    def is_position_in_map(self, x: int, y: int) -> bool:
        return (
            0 <= x <= self.maxPoint[0] and
            0 <= y <= self.maxPoint[1] and
            self.grid[y][x] != "#"
        )
    
    def get_minimum_path_to_exit(self, startingPosition: tuple[int, int], targetPosition: tuple[int, int], startingRound=0) -> int:
        current_positions = set([startingPosition])
        for round in range(startingRound, startingRound+2000):
            next_positions = set()
            for position in current_positions:
                for next_position in ((0,0), (0,1), (0,-1), (1,0), (-1,0)):
                    new_position = (position[0]+next_position[0], position[1]+next_position[1])
                    if (
                        new_position not in next_positions and
                        self.is_position_in_map(new_position[0], new_position[1]) and
                        not self.is_position_in_blizzard(new_position[0], new_position[1], round+1)
                    ):
                        next_positions.add(new_position)
                        if new_position == targetPosition:
                            return round + 1
                current_positions = next_positions

        return -1
    
    def to_string(self, round: int) -> str:
        output = ""
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char == "#":
                    output+="#"
                else:
                    output+=self.gridPoints[(x,y)].to_string(round, maxX = self.maxPoint[0], maxY=self.maxPoint[1])
            output+="\n"
        return output

def parse(data: list[str]) -> Grid:
    return Grid(data)

def solve_1(data):
    grid = parse(data)

    solution = grid.get_minimum_path_to_exit(grid.startingPosition, grid.targetPosition)
    return solution

def solve_2(data):
    grid = parse(data)

    aller = grid.get_minimum_path_to_exit(grid.startingPosition, grid.targetPosition)
    retour = grid.get_minimum_path_to_exit(grid.targetPosition, grid.startingPosition, aller)
    aller_bis = grid.get_minimum_path_to_exit(grid.startingPosition, grid.targetPosition, retour)
    return aller_bis


# check that test data works
out1 = solve_1(test_data)

if out1 != 18:
    print(f"test 1 : {out1} != 18")
    raise Exception("Bad result on test data")

out2 = solve_2(test_data)
if out2 !=54:
    print(f"test 2: {out2} != 54")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 

print(f"result 2: {solve_2(data)}")