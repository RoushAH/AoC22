from collections import deque
from listfuncs import merge

TESTING = True
R = "R"
L = "L"
N = (0,-1)
S = (0,1)
E = (1,0)
W = (-1,0)
dirs = deque([E,S,W,N])
turns = {R:-1, L:1}

filename = "day22sample.txt" if TESTING else "day22.txt"

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.readlines()
    # ingest data, steps first 'cause they're easier
    steps = data[-1].replace(R, " R ").replace(L, " L ")
    steps = steps.split()
    for i in range(len(steps)):
        if i % 2 == 0:
            steps[i] = int(steps[i])
    print(steps)
    # Not sure if I need to pad for movement