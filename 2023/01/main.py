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
    return sum(adventofcode_day1_line(line) for line in text.split("\n"))

# example
adventofcode_day1("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")

# real
adventofcode_day1(data)

def preprocess(line):
    return line.replace("one","one1one").replace("two","two2two").replace("three","three3three").replace("four","four4four").replace("five","five5five").replace("six","six6six").replace("seven","seven7seven").replace("eight","eight8eight").replace("nine","nine9nine").replace("zero","zero0zero")

def adventofcode_day1_part2(text):
    return sum(adventofcode_day1_line(preprocess(line)) for line in text.split("\n"))

adventofcode_day1_part2("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")

# real
adventofcode_day1_part2(data)
