import itertools, math

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

def is_visible_from_outside(d, i, j):
    min_size=d[i][j]

    return not all([
        any(d[ii][j]>= min_size for ii in range(0, i)),
        any(d[ii][j]>= min_size for ii in range(i+1, len(d))),
        any(d[i][jj]>= min_size for jj in range(0, j)),
        any(d[i][jj]>= min_size for jj in range(j+1, len(d[i])))
    ])

def solve_1(d):
    return sum(
        is_visible_from_outside(d, i, j) for i,j in itertools.product(range(len(d)), range(len(d[0])))
    )

def calculate_scenic_score(d, i, j):
    if i==0 or j==0 or i==len(d)-1 or j==len(d[i])-1:
        return 0
    scores = [0,0,0,0]
    for ii in range(i-1,-1, -1):
        scores[0]+=1
        if d[ii][j] >= d[i][j]:
            break
    for ii in range(i+1, len(d)):
        scores[1]+=1
        if d[ii][j] >= d[i][j]:
            break
    for jj in range(j-1, -1, -1):
        scores[2]+=1
        if d[i][jj] >= d[i][j]:
            break
    for jj in range(j+1, len(d[0])):
        scores[3]+=1
        if d[i][jj] >= d[i][j]:
            break
    return math.prod(scores)

def solve_2(d):
    return max(
        calculate_scenic_score(d, i, j) for i,j in itertools.product(range(len(d)), range(len(d[0])))
    )


print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")
