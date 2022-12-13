import os
from functools import cmp_to_key, cache

dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

def parse(d):
    return [ eval(line) for line in d if line.strip() != "" ]

def compare(left, right):
    """
        Compare two objects;
        return -1 if it's in the right order, 1 if it's in the wrong order, 0 if it's inconclusive.
    """

    if type(left) == int and type(right) == int:
        if left < right:
            return -1
        if left > right:
            return 1
        return 0
    if type(left) == list and type(right) == list:    
        for i in range(min(len(left), len(right))):
            out = compare(left[i], right[i])
            if out != 0:
                return out

        # we've run out of items to test, so we compare their sizes now
        return compare(len(left), len(right))

    if type(left) == list and type(right) == int:
        return compare(left, [right])
    
    if type(left) == int and type(right) == list:
        return compare([left], right)

def check_paquets(data):
    """return a list of boolean indicating if the paquets are good or not"""
    return [
        compare(data[ii], data[ii+1])
        for ii in range(0, len(data), 2)
    ]

def solve_1(d):
    data = parse(d)
    checked = check_paquets(data)
    return sum(
        i+1 
        for i in range(len(checked))
        if checked[i] == -1
    )

def solve_2(d):
    data = parse(d)
    A=[[2]]
    B=[[6]]
    data.append(B)
    data.append(A)

    data = sorted(data, key=cmp_to_key(compare))

    if not check_paquets(data):
        print("failed to order paquets...")
        exit(1)

    return (data.index(A) +1) * (data.index(B) +1)

print(f"result 1: {solve_1(data)}") # 5503
print(f"result 2: {solve_2(data)}") # 20952