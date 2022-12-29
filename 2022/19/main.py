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

@dataclass
class RobotBlueprint:
    type: str
    ore: int = 0
    clay: int = 0
    obsidian: int = 0

@dataclass
class Blueprint:
    id: int
    ore_robot: RobotBlueprint
    clay_robot: RobotBlueprint
    obsidian_robot: RobotBlueprint
    geode_robot: RobotBlueprint

    def calculate_max_geode_opened(number_of_rounds=24) -> int:
        """
            Calculate the maximum number of geodes that can be opened in a restricted time.
            We'll find the result by dichotomy, finding out how many robots we need to get our output.
        """

        output = number_of_rounds
        
        total_cost = {
            "ore":0,
            "clay":0,
            "obsidian":0
        }

        return output
    
    def get_all_robots(self) -> Iterator[RobotBlueprint]:
        yield self.ore_robot
        yield self.clay_robot
        yield self.obsidian_robot
        yield self.geode_robot

NUM_CORES = mp.cpu_count()

@dataclass
class Simulation:
    """
        Simulation is the class holding on to one (1) simulation of the run.
    """
    blueprint: Blueprint

    ore_robots = 1
    clay_robots = 0
    obsidian_robots = 0
    geode_robots = 0

    ore = 0
    clay = 0
    obsidian = 0
    geode = 0

    number_of_rounds = 24
    actions_disabled : list[str] = field(default_factory=list) 

    def get_simulations_next_step(self, depth_to_run=1) -> list['Simulation']:
        """
            used in multiprocessing. run the simulation for depth_to_run rounds and returns a list of simulations for the end of the depth.
            returns at most depth_to_run**5 simulations. 
            play with depth_to_run to allow the function to run multiple time in the same thread.
        """
        if self.number_of_rounds <= 0:
            return [self]

        output = []

        for robot in self.blueprint.get_all_robots():
            if robot.type in self.actions_disabled:
                continue
            if self.can_buy(robot) and self.should_buy(robot):
                # simulate what happens if we buy it
                if self.number_of_rounds <=1:
                    # buying at this stage is useless as it won't count
                    continue
                if self.number_of_rounds <= 2 and robot.type != "geode":
                    # buying at this stage anything other than a geode robot is useless
                    continue
                simulation_child = copy.deepcopy(self)
                simulation_child.calculate_profits_end_of_turn()
                simulation_child.buy(robot)
                simulation_child.number_of_rounds-=1
                simulation_child.actions_disabled = []
                output.append(simulation_child)

                # add this action to the disabled actions of the future childs.
                self.actions_disabled.append(robot.type)

        # simulates what happens when we don't buy any robot at this round
        if len(self.actions_disabled) != 4 and len(self.actions_disabled) < 1 + (self.ore_robots>0) + (self.clay_robots>0) + (self.geode_robots>0) + (self.obsidian_robots>0):
            simulation_child = copy.deepcopy(self)
            simulation_child.calculate_profits_end_of_turn()
            simulation_child.number_of_rounds-=1

            output.append(simulation_child)

        if depth_to_run > 1:
            new_output = []
            for simulation in output:
                new_output+=simulation.get_simulations_next_step(depth_to_run=depth_to_run-1)
            output = new_output

        return output
    
    def maximum_geode_atteignable(self) -> int:
        """
            guesstimate how many geodes can be mined from this point, if the only robot built from this point forward was the geode one.
            used to early cancel runs that will lead to nowhere.
            shouldn't be used for high values of number_of_rounds.
        """
        child_simulation = copy.deepcopy(self)
        for n in range(self.number_of_rounds):
            if child_simulation.can_buy(child_simulation.blueprint.geode_robot):
                child_simulation.buy(child_simulation.blueprint.geode_robot)
            child_simulation.calculate_profits_end_of_turn()
        return child_simulation.geode

    def can_buy(self, robot: RobotBlueprint) -> bool:
        """
            indicate if we have the means to buy this robot type.
        """
        return self.ore >= robot.ore and self.clay >= robot.clay and self.obsidian >= robot.obsidian
    
    def should_buy(self, robot: RobotBlueprint) -> bool:
        """
            indicate if it is useful to continue buying this robot type on this simulation.
        """
        if robot.type == "ore":
            return self.ore_robots < max(robot.ore for robot in self.blueprint.get_all_robots())
        if robot.type == "clay":
            return self.clay_robots < max(robot.clay for robot in self.blueprint.get_all_robots())
        if robot.type == "obsidian":
            return self.obsidian_robots < max(robot.obsidian for robot in self.blueprint.get_all_robots())
        return True

    def buy(self, robot: RobotBlueprint):
        """
            buy this robot type and add it to the simulation.
        """
        self.ore -= robot.ore 
        self.clay -= robot.clay 
        self.obsidian -= robot.obsidian

        if robot.type == "ore":
            self.ore_robots+=1
        elif robot.type == "clay":
            self.clay_robots+=1
        elif robot.type == "obsidian":
            self.obsidian_robots+=1
        elif robot.type == "geode":
            self.geode_robots+=1
    
    def calculate_profits_end_of_turn(self):
        """
            calculate the profits realised at the end of the turn.
        """
        self.ore+=self.ore_robots
        self.clay+=self.clay_robots
        self.obsidian+=self.obsidian_robots
        self.geode+=self.geode_robots
    
    def __lt__(self, other):
        # note: this is explicitely inverse than what a true lt should do - this is to have a better sort in the PriorityQueue.
        return self.geode + self.geode_robots * self.number_of_rounds > other.geode + other.geode_robots * other.number_of_rounds

def parse(d: list[str]) -> list[Blueprint]:
    """
        Parse the input strings into custom objects.
    """
    output: list[Blueprint] = []
    regex = r"Blueprint (?P<id>\d+): Each ore robot costs (?P<ore_ore>\d+) ore. Each clay robot costs (?P<clay_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay. Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian."
    for line in d:
        match = re.fullmatch(regex, line)
        if match is None:
            raise Exception("could'n't parse line", line)

        output.append(
            Blueprint(
                id = int(match.group('id')),
                ore_robot = RobotBlueprint(type="ore", ore = int(match.group('ore_ore'))),
                clay_robot = RobotBlueprint(type="clay", ore = int(match.group('clay_ore'))),
                obsidian_robot = RobotBlueprint(type="obsidian", ore = int(match.group('obsidian_ore')), clay=int(match.group('obsidian_clay'))),
                geode_robot = RobotBlueprint(type="geode", ore=int(match.group('geode_ore')), obsidian=int(match.group('geode_obsidian'))),
            )
        )
    return output

class MyManager(SyncManager):
    # cf https://stackoverflow.com/questions/25324560/strange-queue-priorityqueue-behaviour-with-multiprocessing-in-python-2-7-6
    pass
MyManager.register("PriorityQueue", PriorityQueue)
def Manager():
    m = MyManager()
    m.start()
    return m

def get_maximum_turn_geodes_reachable(number_of_geodes):
    """
        return the maximum round number at which a geode robot can be created to build at least the number_of_geodes.
    """

    for i in range(1, 32):
        if i * (i+1) / 2 > number_of_geodes:
            return i
    
    return 0


def mp_worker_simulation(simulation_queue: PriorityQueue[tuple[int, Simulation]], maximum_atteigned : mp.Value):
    while True:
        try:
            priority, simulation = simulation_queue.get(timeout=60)
            # print(f"picked {priority:02} / {simulation.geode} at {time.time()}")
        except Empty:
            return
        new_simulations = simulation.get_simulations_next_step(depth_to_run=3)
        for new_simulation in new_simulations:
            if new_simulation.number_of_rounds <=0:
                if maximum_atteigned.value < new_simulation.geode:
                    # print(f"new maximum atteigned : {new_simulation.geode}")
                    maximum_atteigned.value = new_simulation.geode
            else:
                if (
                    new_simulation.number_of_rounds < 2 + get_maximum_turn_geodes_reachable(maximum_atteigned.value) and
                    new_simulation.maximum_geode_atteignable() + 2 < maximum_atteigned.value
                ):
                    # abort this run entirely.
                    continue
                simulation_queue.put((new_simulation.number_of_rounds, new_simulation))
        simulation_queue.task_done()

def solve_1(data):
    blueprints = parse(data)
    solutions = solve(blueprints, number_minutes=24)
    return sum([
        (i+1) * s
        for i, s in enumerate(solutions)
    ])

def solve_2(data):
    blueprints = parse(data)
    if len(blueprints) > 3:
        blueprints = blueprints[:3]
    solutions = solve(blueprints, number_minutes=32)
    return math.prod([
        s
        for i, s in enumerate(solutions)
    ])

def solve(blueprints, number_minutes=24) -> list[int]:
    output = []

    # multiprocessing variables
    m = Manager()
    # sim_queue contains the queue for all simulations
    sim_queue = m.PriorityQueue()
    # maximum_ateigned contains the highest value reached by the current simulation; should be reset to 0 after a run.
    maximum_atteigned = mp.Value('i',0)

    # start the processes
    processes = []
    for i in range(8):
        proc = mp.Process(target=mp_worker_simulation, args=[sim_queue, maximum_atteigned])
        processes.append(proc)
        proc.start()

    # start the work on the workers
    for blueprint in blueprints:
        simulation = Simulation(blueprint)
        simulation.number_of_rounds = number_minutes

        # reset the maximum atteigned value to 0
        maximum_atteigned.value = 0
        
        # put the work in
        sim_queue.put((number_minutes, simulation))
        print("starting processes for blueprint", blueprint.id)

        # wait for queue to be absorbed
        sim_queue.join()

        output.append(maximum_atteigned.value)
    
    # end the processes
    for proc in processes:
        proc.kill()
    return output

# check that test data works
out1 = solve_1(test_data)

if out1 != 33:
    print(f"test : {out1} != 33")
    raise Exception("Bad result on test data")

out2 = solve_2(test_data)
if out2 != 62 * 56:
    print(f"test : {out2} != ?")
    raise Exception("Bad result on test data")

print("tests passed")

print(f"result 1: {solve_1(data)}") 

print(f"result 2: {solve_2(data)}")