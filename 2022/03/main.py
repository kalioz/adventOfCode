import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as one string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data= "".join(fi.readlines())

def priority(letter):
    if letter.isupper():
        return ord(letter)-ord('A')+27
    return ord(letter)-ord('a')+1

def solve_1(d):
    c=0
    for line in d.split('\n'):
        if len(line) == 0:
            continue
        ll = int(len(line) / 2)
        l0 = line[:ll]
        l1 = line[ll:]
        intersect = set(l0).intersection(l1)
        match = intersect.pop()
        c+= priority(match)
    return c

def solve_2(d):
    c=0
    lines = d.split('\n')
    for ll in range(0, len(lines), 3):
        if lines[ll] == "":
            continue
        i1 = set(lines[ll]).intersection(lines[ll+1])
        i2 = i1.intersection(lines[ll+2])
        match = i2.pop()
        c+=priority(match)
    return c

print(f"1st response: {solve_1(data)}")
print(f"2nd response: {solve_2(data)}")