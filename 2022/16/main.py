import os, math, time, re
import copy

from multiprocessing import Pool, SimpleQueue, cpu_count
from functools import partial
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./test_data"), 'r') as fi:
    test_data = "".join(fi.readlines())
    test_data = test_data.split('\n')

with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')

def parse(d):
    output = {}
    for line in d:
        n = {
                "id": line.split(' ')[1],
                "flow_rate": int(line.split('rate=')[1].split(';')[0]),
                "tunnels": "".join(line.split(' ')[9:]).replace(' ', '').split(','),
                "distanceTo": {}
            }
        output[n['id']] = n
    return output


def calculate_distance(graph, p1, p2, _ignore_positions=None):
    if p2 in graph[p1]["tunnels"]:
        return 1

    if _ignore_positions is None:
        _ignore_positions = set()
    else: 
        _ignore_positions = _ignore_positions.copy()

    _ignore_positions.add(p1)
    _ignore_positions.add(p2)

    distances = [calculate_distance(graph, p3,p2, _ignore_positions=_ignore_positions) for p3 in graph[p1]["tunnels"] if p3 not in _ignore_positions]

    if len(distances) == 0:
        # happens when we're in a loop - return a big distance to throw this run
        return len(graph)**2

    return 1 + min(distances)

def calculate_path_length(graph, path):
    return sum(
        graph[path[i]]["distanceTo"][path[i+1]] for i in range(len(path)-1) 
    )

def explore(graph, current_position="AA", current_path=["AA"], max_distance=30):
    distance = calculate_path_length(graph, current_path) + sum(graph[position]["flow_rate"]>0 for position in current_path)

    if distance >= max_distance:
        return 0, current_path
    
    possible_gains = [
        {
            "position": next_pos,
            "value": graph[next_pos]["flow_rate"] * (max_distance - distance - graph[current_position]["distanceTo"][next_pos])
        }
        for next_pos in graph if next_pos not in current_path
    ]

    possible_gains.sort(key=lambda x: x["value"], reverse=True)
    possible_gains = [p for p in possible_gains if p["value"] > 0]
    
    max_result = 0
    max_path = current_path
    
    for i in range(min(6, len(possible_gains))):
        possible_gain = possible_gains[i]
        possible_gain_result, possible_gain_path = explore(
            graph,
            current_position=possible_gain["position"],
            current_path=current_path+[possible_gain["position"]],
            max_distance=max_distance)

        if possible_gain_result > max_result:
            max_result = possible_gain_result
            max_path = possible_gain_path
    
    return max_result + graph[current_position]["flow_rate"] * (max_distance - distance), max_path


def solve_1(d):
    graph = parse(d)

    positions_useful=[_id for _id in graph if graph[_id]["flow_rate"] > 0]
    positions_useful.append("AA") # add starting position too only for the distance calcul
    # calculate min distance between each useful position
    for i1 in range(len(positions_useful)):
        p1 = graph[positions_useful[i1]]
        for i2 in range(i1+1, len(positions_useful)):
            p2 = graph[positions_useful[i2]]
            distance = calculate_distance(graph, p1["id"], p2["id"])
            p1["distanceTo"][p2["id"]] = distance
            p2["distanceTo"][p1["id"]] = distance

    useful_graph = {
        key: graph[key] for key in graph if key in positions_useful
    }

    return explore(useful_graph)[0]
    



out1 = solve_1(test_data)
if out1 != 1651:
    print(f"test : {out1} != 1651")
    raise Exception("Bad result on test data")

# if solve_2(test_data, 20) != 56000011:
#     print(f"test : {solve_2(test_data, 20)} != 56000011")
#     raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 
# 5394083 too high
# 5733733
# print(f"result 2: {solve_2(data)}") # 11583882601918