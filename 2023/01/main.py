import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as one string
with open(os.path.join(dir_path, "./data.txt"), 'r') as fi:
    data= "".join(fi.readlines())

data = data.strip()

def adventofcode_day1_line(line):
    first = None
    for i in line:
        if i in "0123456789":
            first = i
            break
    last = None
    for i in range(len(line)-1, -1, -1):
        if line[i] in "0123456789":
            last = line[i]
            break
    return int(f"{first}{last}")

def adventofcode_day1(text):
    return sum(adventofcode_day1(line) for line in ftext.split("\n"))

# example
adventofcode_day1_full("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")

# real
adventofcode_day1_full(data)
