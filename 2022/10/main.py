import itertools, math

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# read data as a single string
with open(os.path.join(dir_path, "./data"), 'r') as fi:
    data = "".join(fi.readlines())
    data = data.split('\n')


def crt_print(i, x):
    if i%40 == 0:
        print('\n', end="")
    print("#" if i%40 in [x-1, x, x+1] else " ", end="")

def solve(d):
    x=1
    histo_x=[x]
    for line in d:
        if line == "noop":
            # 1st cycle
            crt_print(len(histo_x)-1, x)
            histo_x.append(x)
            continue
        else:
            # 1st cycle
            crt_print(len(histo_x)-1, x)
            histo_x.append(x)

            # 2nd cycle
            crt_print(len(histo_x)-1, x)
            x+=int(line.split(' ')[1])
            histo_x.append(x)

    # solve 1 :
    return sum(i * histo_x[i-1] for i in range(20, 220+1, 40))


print(f"1st response: {solve(data)}")
# print(f"2nd response: {solve(data, 10)}")