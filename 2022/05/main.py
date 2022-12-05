import os
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())

def parser_init(data):
    init_data = data.split('\n\n')[0]
    first_line_len = len(data.split('\n')[0])
    n_data = int(first_line_len / 4)
    output = [""] * (n_data +1)

    for line in init_data.split('\n'):
        if line[1] == "1":
            continue
        j=-1
        for i in range(1, len(line), 4):
            j+=1
            if line[i] != " ":
                output[j]+= line[i]
    
    for i in range(len(output)):
        output[i] = output[i][::-1]
    
    return output

def parser_instruction_line_1(data, line):
    l = line.split(' ')
    move_n, move_from, move_to = int(l[1]), int(l[3]), int(l[5])
    data[move_to-1] = data[move_to-1] + data[move_from-1][-move_n:][::-1]
    data[move_from-1] = data[move_from-1][:-move_n]
    return data

def solve_1(d):
    data_tmp = parser_init(data)
    instructions_lines = data.split('\n\n')[1]
    for line in instructions_lines.split('\n'):
        data_tmp = parser_instruction_line_1(data_tmp, line)
    
    return "".join([d[-1] for d in data_tmp])

def parser_instruction_line_2(data, line):
    l = line.split(' ')
    move_n, move_from, move_to = int(l[1]), int(l[3]), int(l[5])
    data[move_to-1] = data[move_to-1] + data[move_from-1][-move_n:]
    data[move_from-1] = data[move_from-1][:-move_n]
    return data

def solve_2(d):
    data_tmp = parser_init(data)
    instructions_lines = data.split('\n\n')[1]
    for line in instructions_lines.split('\n'):
        data_tmp = parser_instruction_line_2(data_tmp, line)
    
    return "".join([d[-1] for d in data_tmp])

print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")