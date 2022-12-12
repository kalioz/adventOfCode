import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

def can_reach(a,b):
    if a == "S":
        a = "a"
    if b == "S":
        b = "a"
    if a == "E":
        a = "z"
    if b == "E":
        b = "z"
    
    return ord(b)-ord(a) <= 1

def find_position(data, letter):
    d="".join(data)
    return (int(d.index(letter) // len(data[0])), int(d.index(letter) % len(data[0])))

def solve_1(m):
    # Uses dijkstra to solve the issue, from start to finish
    solved_map=[None] * len(m) # map with the # of steps required to access the tile
    for i in range(len(m)):
        solved_map[i] = [None] * len(m[i])
    
    position_start = find_position(data, "S")
    position_end = find_position(data, "E")

    solved_map[position_start[0]][position_start[1]] = 0
    points_to_solve=[position_start]

    while len(points_to_solve) > 0:
        tmp_points_to_solve=[]
        for i,j in points_to_solve:
            for ii, jj in ((i,j+1),(i, j-1), (i+1, j), (i-1, j)):
                if ii < 0 or jj < 0 or ii > len(m)-1 or jj > len(m[0])-1:
                    continue
                if can_reach(m[i][j], m[ii][jj]) and solved_map[ii][jj] is None:
                    solved_map[ii][jj] = solved_map[i][j]+1
                    tmp_points_to_solve.append((ii, jj))

        points_to_solve = tmp_points_to_solve
    
    return solved_map[position_end[0]][position_end[1]]

def solve_2(m):
    # Use dijkstra to solve, from the end to the first found case with a value of "a"
    # since we're using a propagation algorithm, the first "a" we find is also the closest one
    # note we've inverted the can_reach function, so that we're still technically finding the best way from the "a" to the End, but backwards.

    solved_map=[None] * len(m) # map with the # of steps required to access the tile
    for i in range(len(m)):
        solved_map[i] = [None] * len(m[i])

    m_str = "".join(m)

    position_end = find_position(data, "E")

    solved_map[position_end[0]][position_end[1]] = 0

    output=999999999999
    
    points_to_solve=[position_end]
    while len(points_to_solve) > 0:
        tmp_points_to_solve=[]
        for i,j in points_to_solve:
            # print(i,j)
            for ii, jj in ((i,j+1),(i, j-1), (i+1, j), (i-1, j)):
                if ii < 0 or jj < 0 or ii > len(m)-1 or jj > len(m[0])-1:
                    continue
                # note we inverted the can_reach function as we start from the end.
                if can_reach(m[ii][jj], m[i][j]) and solved_map[ii][jj] is None:
                    if solved_map[i][j]+1 < output and m[ii][jj] == "a":
                        output = solved_map[i][j]+1
                        break
                    solved_map[ii][jj] = solved_map[i][j]+1
                    tmp_points_to_solve.append((ii, jj))

        points_to_solve = tmp_points_to_solve

    
    
    return output

print(solve_1(data))
print(solve_2(data))