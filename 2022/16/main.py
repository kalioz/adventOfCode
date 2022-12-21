import os, math, time, re
import copy
import itertools

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
    ) + sum(graph[position]["flow_rate"]>0 for position in path)


def calculate_path_worth(graph, path, max_depth):
    out = 0
    depth = 1
    # we assume path[0] is "AA" and won't be activated
    for i in range(1, len(path)):
        depth+=graph[path[i-1]]["distanceTo"][path[i]]
        out+=(max_depth - depth) * graph[path[i]]["flow_rate"]
        depth+=1
    
    return out


def explore(graph, current_positions=["AA"], current_paths=[["AA"]], max_distance=30):
    distances = [
        calculate_path_length(graph, current_paths[i])
        for i in range(len(current_paths))
    ]

    visited_positions = list(itertools.chain(*current_paths))

    if min(distances) >= max_distance: # end of calculus
        return 0, current_paths
    
    possible_gains = []

    for player_i in range(len(current_positions)):
        possible_gains+= [
            {
                "player_i": player_i,
                "position": next_pos,
                "value": calculate_path_worth(graph, current_paths[player_i]+[next_pos], max_distance)
            }
            for next_pos in graph if next_pos not in visited_positions
        ]

    possible_gains.sort(key=lambda x: x["value"], reverse=True)
    possible_gains = [p for p in possible_gains if p["value"] > 0]
    
    max_result = graph[current_positions[0]]["flow_rate"] * (max_distance - distances[0]) # TODO : on multi n, risk of counting twice the same case

    max_path = current_paths
    
    # N.B.: we arbitraly reduce the number of possibilities to consider to the top 6 best.
    for i in range(min(4, len(possible_gains))):
        possible_gain = possible_gains[i]
        player_i = possible_gain["player_i"]

        current_paths_c = list(current_paths)
        current_paths_c[player_i] = current_paths_c[player_i] + [possible_gain["position"]] # note: we're using this to change the ID of the list.

        current_positions_c= list(current_positions)
        current_positions_c[player_i] = possible_gain["position"]

        possible_gain_result, possible_gain_paths = explore(
            graph,
            current_positions=current_positions_c,
            current_paths=current_paths_c,
            max_distance=max_distance
        )

        # N.B: we recalculate this value because we did an error somewhere in the previous calculus, and I can't find it :D
        possible_gain_result = sum([calculate_path_worth(graph, possible_gain_paths[i], max_distance) for i in range(len(possible_gain_paths))])

        if possible_gain_result > max_result:
            max_result = possible_gain_result
            max_path = possible_gain_paths
    
    max_result = sum([calculate_path_worth(graph, max_path[i], max_distance) for i in range(len(max_path))])

    return max_result, max_path


def solve(d, n=1):
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

    current_positions=["AA"]
    current_paths=[["AA"]]
    max_distance=30

    if n == 2:
        current_positions=["AA", "AA"]
        current_paths=[["AA"], ["AA"]]
        max_distance=26

    result = explore(useful_graph, current_positions=current_positions, current_paths=current_paths, max_distance=max_distance)

    result_computed = sum([calculate_path_worth(useful_graph, result[1][i], max_distance) for i in range(len(result[1]))])

    if result_computed != result[0]:
        print("error")
        exit(1)

    return result[0]
    



out1 = solve(test_data)
if out1 != 1651:
    print(f"test : {out1} != 1651")
    raise Exception("Bad result on test data")

out2 = solve(test_data, n=2)
if out2 != 1707:
    print(f"test : {out2} != 1707")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve(data)}") 

print(f"result 2: {solve(data, n=2)}")