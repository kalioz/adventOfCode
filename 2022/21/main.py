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

def parse(d: list[str]) -> dict[str]:
    """
        Parse the input strings into custom objects.
    """
    output = {}
    for line in d:
        name, content=line.split(':')
        if content.strip().count(' ') == 0:
            content = int(content)
        output[name] = content

    return output

def reduce(parsed_data: dict[str], key) -> int:
    """
        return the result to the operation to find the numeric value of key.
    """
    if type(parsed_data[key]) == int:
        return parsed_data[key]
    
    vals = parsed_data[key].strip().split(' ')
    val0 = reduce(parsed_data, vals[0])
    operator = vals[1]
    val1 = reduce(parsed_data, vals[2])

    return eval(f"{val0} {operator} {val1}")
    

def solve_1(d) -> int:
    parsed_data = parse(d)

    return int(reduce(parsed_data, 'root'))

def toSingleOperation(parsed_data, key) -> bool:
    """
        reduce the content of the key to a single operation, without any int value
    """
    if type(parsed_data[key]) == int:
        return key
    
    vals = parsed_data[key].strip().split(' ')
    val0 = toSingleOperation(parsed_data, vals[0])
    operator = vals[1]
    val1 = toSingleOperation(parsed_data, vals[2])

    return f"({val0} {operator} {val1})"

def findLastOperationToBeDone(op) -> tuple:
    """
        calculate the last operation that would be done in a mathematical sense
        e.g. (((a+b) * 5) + 3) would give ["((a+b) * 5)", '+', '3']

        /!\ assumes every operation is behind parenthesis
    """
    op = op.strip()
    # remove useless parenthesis
    if op[0] == "(" and op[-1] == ")":
        op = op[1:-1]
    
    depth = 0

    for i, char in enumerate(op):
        if char == "(":
            depth+=1
        elif char == ")":
            depth-=1
        elif depth == 0 and char in "+-*/":
            return (op[:i].strip(), char, op[i+1:].strip())
    
    return op
    


def solve_2(d):
    parsed_data = parse(d)
    
    vals = parsed_data['root'].strip().split(' ')
    leftside = vals[0]
    rightside = vals[2]

    singleOperations = [toSingleOperation(parsed_data, leftside), toSingleOperation(parsed_data, rightside)]

    if "humn" not in singleOperations[0]:
        singleOperations = singleOperations[::-1]
    
    # humn is now in the leftside of the comparison, and will stay there while we reverse the mechanism

    while singleOperations[0] != "humn":
        op = singleOperations[0]
        lastOp = findLastOperationToBeDone(op)
        human_is_left_side = "humn" in lastOp[0]

        if human_is_left_side:
            singleOperations[0] = lastOp[0]
        else:
            singleOperations[0] = lastOp[2]

        if lastOp[1] in "+*":
            newOp = "-/"["+*".index(lastOp[1])]
            if human_is_left_side:
                singleOperations[1] = f"({singleOperations[1]} {newOp} {lastOp[2]})"
            else:
                singleOperations[1] = f"({singleOperations[1]} {newOp} {lastOp[0]})"
        elif lastOp[1] in "-/":
            if human_is_left_side:
                newOp = "+*"["-/".index(lastOp[1])]
                singleOperations[1] = f"({singleOperations[1]} {newOp} {lastOp[2]})"
            else:
                singleOperations[1] = f"({lastOp[0]} {lastOp[1]} {singleOperations[1]})"
    
    return int(eval(singleOperations[1], parsed_data))

# check that test data works
out1 = solve_1(test_data)

if out1 != 152:
    print(f"test 1 : {out1} != 152")
    raise Exception("Bad result on test data")

out2 = solve_2(test_data)
if out2 != 301:
    print(f"test 2 : {out2} != ?")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 

print(f"result 2: {solve_2(data)}")