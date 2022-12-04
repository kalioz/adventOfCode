import os
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = fi.readlines()
    data = [d.replace('\n', '') for d in data if len(d) != 0]

def parser(l):
    regex=r"(\d+)-(\d+),(\d+)-(\d+)"
    match = re.search(regex, l)
    return list(int(match.group(i)) for i in range(1,5))


def solve_1(d):
    c=0
    for line in d:
        if len(line) == 0:
            continue
        
        r=parser(line)
        if (r[0]-r[2]) * (r[1]-r[3]) <= 0:
            c+=1
    return c

def solve_2(d):
    c=0
    for line in d:
        if len(line) == 0:
            continue
        
        r=parser(line)
        if r[2] <= r[0] <= r[3] or r[0] <= r[2] <= r[1]:
            c+=1
    return c

print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")