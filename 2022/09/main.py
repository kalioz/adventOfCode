import itertools, math

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

directions= {
    'U': (1,0),
    'D': (-1,0),
    'L': (0,-1),
    'R': (0,1)
}

def calculate_new_position_tail(head, tail):
    if math.dist(head, tail) == 2: # line
        return (
            int((head[0]+tail[0])/2),
            int((head[1]+tail[1])/2)
        )
    elif math.dist(head, tail) > 1.5: # diagonal
        return (
            tail[0] + ( 1 - 2 * (head[0] < tail[0])),
            tail[1] + ( 1 - 2 * (head[1] < tail[1])),
        )
    return tail

def solve(d, rope_length=2):
    rope = [(0,0)] * rope_length
    pos_tail_positions=[rope[-1]]
    for line in d:
        direction, n = line.split(' ')
        for _ in range(int(n)):
            # calculate new positions
            # head of the rope
            rope[0]=(rope[0][0]+directions[direction][0], rope[0][1]+directions[direction][1])
            # rest of the rope
            for i in range(1, len(rope)):
                rope[i]=calculate_new_position_tail(rope[i-1], rope[i])
            
            pos_tail_positions.append(rope[-1])

    return len(set(pos_tail_positions))


print(f"1st response: {solve(data, 2)}")
print(f"2nd response: {solve(data, 10)}")