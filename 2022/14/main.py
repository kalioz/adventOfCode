import os, math, time
from functools import cmp_to_key, cache

dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

def parse(d):
    output = {
        (500,0) : "+"
    }
    for line in d:
        positions = line.split(' -> ')
        for i in range(len(positions)-1):
            pos0 = eval(positions[i])
            pos1 = eval(positions[i+1])
            dist = int(math.dist(pos0, pos1))
            for j in range(dist+1):
                xx, yy = (pos1[0] - pos0[0]) * j / dist, (pos1[1] - pos0[1]) * j / dist
                x,y = int(pos0[0] + xx), int(pos0[1] + yy)
                output[(x,y)] = "#"
    
    return output

class Terrain:
    def __init__(self, dict_of_positions: dict, floor_present=False) -> None:
        self.dict_of_positions = dict_of_positions
        self.floor_present = floor_present
        self.calculate_min_max()

        self.floor_position = self.maxY + 2 * self.floor_present
    
    def calculate_min_max(self):        
        keys = sorted(list(self.dict_of_positions.keys()), key= lambda a: (a[1], a[0]))
        self.minX = min(keys, key= lambda x: x[0])[0]
        self.maxX = max(keys, key= lambda x: x[0])[0]
        self.minY = min(keys, key= lambda x: x[1])[1]
        self.maxY = max(keys, key= lambda x: x[1])[1]


    def is_inside_boundaries(self, point: tuple[int, int]):
        return self.floor_position >= point[1]
    
    def is_position_taken(self, point: tuple[int, int]):
        return point in self.dict_of_positions or (self.floor_present and point[1] == self.floor_position)

    def set_new_grain_position(self, point: tuple[int, int]):
        """
            find the position for a grain originating at point, and place it in the Terrain.
            return True if a new position was found, False if it falls out of bounds.
        """
        # check if position is already taken by a grain of sand
        if point in self.dict_of_positions and self.dict_of_positions[point] == "o":
            return None

        while self.is_inside_boundaries(point):
            if not self.is_position_taken((point[0], point[1]+1)):
                point=(point[0], point[1]+1)
            elif not self.is_position_taken((point[0]-1, point[1]+1)):
                point=(point[0]-1, point[1]+1)
            elif not self.is_position_taken((point[0]+1, point[1]+1)):
                point=(point[0]+1, point[1]+1)
            else:
                self.dict_of_positions[point] = "o"
                self.calculate_min_max()
                return True
        
        return False

    def dict2map(self):
        """
            Convert a dict of positions to a list of list containing the positions.
        """
        self.calculate_min_max()
        m = self.dict_of_positions
        keys = sorted(list(m.keys()), key= lambda a: (a[1], a[0]))
        output = [None] * (self.maxY - self.minY+1)
        for line in range(len(output)):
            output[line] = [" "] * (self.maxX-self.minX+1)
        
        for key in keys:
            output[key[1]-self.minY][key[0]-self.minX] = m[key]
        
        return output
    
    def __str__(self) -> str:
        tmp = self.dict2map()
        output= "\n".join("".join(line) for line in tmp)
        if self.floor_present:
            output+="\n"+"=" * len(tmp[-1])
        return output

def solve_1(d):
    m = parse(d)
    t = Terrain(m)
    
    while t.set_new_grain_position((500,0)):
        continue

    print(t)

    return str(t).count("o")

def solve_2(d):
    m = parse(d)
    t = Terrain(m, floor_present=True)

    # instead of simulating each grain's descent, we're going under the assumption the grain at (500,0) exists, which means it is supported by 3 grains below, who themselves are supported by other grains.

    new_grain_positions=[(500,0)]
    t.dict_of_positions[(500,0)] = "o"

    while len(new_grain_positions) > 0:
        tmp = []
        for grain_position in new_grain_positions:
            for d in [(-1,1), (0, 1), (1, 1)]:
                new_pos = (grain_position[0]+d[0], grain_position[1]+d[1])
                if not t.is_position_taken(new_pos):
                    t.dict_of_positions[new_pos] = "o"
                    tmp.append(new_pos)
        new_grain_positions = tmp

    # print(t)

    return str(t).count("o")


print(f"result 1: {solve_1(data)}")
print(f"result 2: {solve_2(data)}")