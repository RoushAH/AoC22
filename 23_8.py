import math

TESTING = False
filename = "data/23_8_sample.txt" if TESTING else "data/23_8.txt"
nodes = {}
steps = ""


class Node:
    def __init__(self, value):
        self.name = value[:3]
        tup = value.split(" = ")[1][1:-1].split(", ")
        self.L = tup[0]
        self.R = tup[1]
        self.string_val = value

    def __str__(self):
        return str(self.string_val)

    def follow(self, direction):
        if direction == "L":
            return self.L
        elif direction == "R":
            return self.R
        else:
            return False

def check_current(nodes):
    for node in nodes:
        if not node.endswith("Z"):
            return False
    return True

def follow_trail(starter):
    current = starter
    step = 0
    while not current.endswith("Z"):
        current = nodes[current].follow(steps[step % len(steps)])
        step += 1
    return step

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    # assemble a dict of "nodes"
    steps = data[0]
    for datum in data[2:]:
        nodes[datum[:3]] = Node(datum)

    # current = "AAA"
    step = follow_trail("AAA")
    print(f"Part 1 answer: {step}")
    # Ghost mode!
    # 1 -- Identify starting points
    starters = []
    enders = []
    for node in nodes:
        if node.endswith("Z"):
            enders.append(node)
        elif node.endswith("A"):
            starters.append(node)
    print(f"\nStarters: {starters}\nEnders: {enders}")
    # 2 -- Determine steps for each to a possible ender ASSUMING that each travels in a loop
    lengths = {name:0 for name in starters}
    for starter in starters:
        lengths[starter] = follow_trail(starter)
    print(f"\nLengths: {lengths}\n")
    score = math.lcm(*list(lengths.values()))
    print(f"Score: {score}")
    # 3 -- Determine LCM for each

