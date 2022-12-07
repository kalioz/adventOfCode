import os
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())

def parse_data(d):
    """
        read the data and return a dict of files and their size
        output : {"path/to/file": 48}
    """
    curdir="/"
    files = {}
    instructions = d.split('\n$')
    for instruction in instructions:
        cmd = instruction.split('\n')[0]
        results = instruction.split('\n')[1:]

        cmd_str = cmd.strip().split(' ')[0]
        
        if cmd_str == 'cd':
            cmd_arg = cmd.strip().split(' ')[1]
            if cmd_arg.startswith('/'):
                curdir = cmd_arg
            elif cmd_arg == "..":
                curdir = os.path.split(curdir)[0]
            else:
                curdir = os.path.join(curdir, cmd_arg)
        elif cmd_str == 'ls':
            for line in results:
                line = line.strip()
                if line.startswith('dir'):
                    continue
                else:
                    file_size, filename = line.split(' ')
                    files[os.path.join(curdir, filename)] = int(file_size)
    
    return files

def list_directories(files):
    output = set()
    for file in files:
        while file != "/":
            file = os.path.split(file)[0]
            output.add(file)
    return output


def find_directories_sizes(files):
    directories = list_directories(files)
    directory_sizes = {
        d: sum(files[i] for i in files if i.startswith(d)) for d in directories
    }

    return directory_sizes
    

def solve_1(d):
    files = parse_data(d)
    dir_sizes = find_directories_sizes(files)
    return sum(i for i in list(dir_sizes.values()) if i < 100000)

def solve_2(d):
    files = parse_data(d)
    dir_sizes = find_directories_sizes(files)

    disk_size = 70000000
    needed_size = 30000000
    used_size = dir_sizes['/']
    needed_size_removal = used_size - (disk_size - needed_size)

    return min(i for i in list(dir_sizes.values()) if i > needed_size_removal)


print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")