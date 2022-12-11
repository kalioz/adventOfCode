import itertools, math

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n\n')

def parse(data):
    output = []
    for monkey in data:
        monkey_output={}
        for line in monkey.split('\n'):
            if "Monkey" in line:
                monkey_output['id'] = int(line.split(' ')[1].replace(':',''))
            elif "Starting items" in line:
                monkey_output["items"] = list(int(i) for i in line.split(':')[1].split(','))
            elif "Operation" in line:
                monkey_output['operation'] = line.split('=')[1]
            elif "Test" in line:
                monkey_output['test'] = int(line.split(' ')[-1])
            elif "If true" in line:
                monkey_output['if_true'] = int(line[-1])
            elif "If false" in line:
                monkey_output['if_false'] = int(line[-1])
            else:
                print(f"ERROR: couldn't parse line: {line}")
                exit(1)
        
        output.append(monkey_output)
    return output

def solve(d, rounds=20, worry_divider=3):
    monkeys = parse(d)

    # the numbers will be too big to handle : we only needs the numbers up to the least common multiple used in the tests.
    common_multiple= math.lcm(*[monkey['test'] for monkey in monkeys])

    print(f"common multiple : {common_multiple}")
    
    hitory_item_inspected=[0] * len(monkeys)
    for round in range(rounds):
        for monkey_id in range(len(monkeys)):
            monkey = monkeys[monkey_id]
            
            hitory_item_inspected[monkey_id]+=len(monkey['items'])
            for item in monkey['items']:
                # reduce the value of the item, to handle int overflow
                if item > common_multiple:
                    item = item % common_multiple

                # monkey inspect the item
                old=item
                item = eval(monkey['operation'])
                # monkey didn't damage the item, so less worry on it
                item = int(item / worry_divider)
                if item % monkey['test'] == 0:
                    monkeys[monkey["if_true"]]['items'].append(item)
                else:
                    monkeys[monkey["if_false"]]['items'].append(item)
            
            # monkey has thrown all items
            monkey['items'] = []

    # sort it to get the two biggest one
    hitory_item_inspected = sorted(hitory_item_inspected)

    return hitory_item_inspected[-1] * hitory_item_inspected[-2]


print(f"1st response: {solve(data)}")
print(f"2nd response: {solve(data, rounds=10000, worry_divider=1)}")