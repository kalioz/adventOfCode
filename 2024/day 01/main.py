inputfile="real.txt"

with open(inputfile, 'r') as fi:
    data = fi.read()

data = data.strip()

def day01_01(data):
    list_a=[]
    list_b=[]
    for line in data.split('\n'):
        list_a.append(int(line.split(' ')[0]))
        list_b.append(int(line.split(' ')[-1]))
    
    list_a.sort()
    list_b.sort()

    return sum(abs(a - b) for a, b in zip(list_a, list_b))

def day01_02(data):
    list_a=[]
    list_b=[]
    for line in data.split('\n'):
        list_a.append(int(line.split(' ')[0]))
        list_b.append(int(line.split(' ')[-1]))
    
    list_a.sort()
    list_b.sort()

    return sum(a*list_b.count(a) for a in list_a)

print(day01_01(data))
print(day01_02(data))

