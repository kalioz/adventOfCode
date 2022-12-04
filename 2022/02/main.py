import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as one string, removing all space chars
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data= "".join(fi.readlines())
    data = data.replace(" ", "")

#ABC 
#XYZ


def solve_1(d):
    c=0
    for line in data.split('\n'):
        if line == "":
            continue
        c+="XYZ".index(line[1])+1
        if line in ["AY","BZ","CX"]:
            c+=6
        elif line in ["AX", "BY", "CZ"]:
            c+=3
    return c

def solve_2(d):
    c=0
    for line in data.split('\n'):
        if line == "":
            continue
        c+="XYZ".index(line[1])*3 + ("ABC".index(line[0]) + ("XYZ".index(line[1]) - 1)) % 3 + 1
    return c

print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")