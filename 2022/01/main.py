import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as one string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data= "".join(fi.readlines())

solver = lambda d,n:sum(sorted(sum(int(i)for i in j.split('\n')if i)for j in d.split('\n\n'))[-n:])

print(f"1st elves carry {solver(data, 1)} calories")
print(f"the first 3 elves carry {solver(data, 3)} calories")