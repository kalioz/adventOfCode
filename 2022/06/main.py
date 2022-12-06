import os
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())

def solve(d, n):
    for c in range(n, len(d)):
        if len(d[c-n:c]) == len(set(d[c-n:c])):
            break
    else:
        print("not found")
        return -1
    return c

print(f"1st response: {solve(data, 4)}")
print(f"2nd response: {solve(data, 14)}")