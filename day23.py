from collections import deque
from listfuncs import merge
from functools import lru_cache

BLANK = "."
ELF = "#"
TESTING = False
DIRECTION_VALUES = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
DIR_DEQUE = deque(["N","S","W","E"])
DIRECTION_LOCATIONS = {"S":(0, 1, 2), "N":(5, 6, 7), "E":(0, 3, 5), "W":(2, 4, 7)}
ELVES = []  # List of current elf locations
PROPOSAL_COUNT = {}  # Dict of proposed_location, num_proposals pairs
PROPOSAL = {}

filename = "data/day23sample.txt" if TESTING else "data/day23.txt"

def display_elves():
    min_x, min_y, max_x, max_y = find_result()
    offset_x = min(min_x, 0)
    offset_y = min(min_y, 0)
    out_array = [[BLANK for x in range(offset_x, max_x + 1)] for y in range(offset_y, max_y + 1)]
    for elf in ELVES:
        out_array[elf[1]+offset_y][elf[0]+offset_x] = ELF

    out_string = ["".join(row) for row in out_array]
    out_string = "\n".join(out_string)
    print(out_string,"\n\n")

def register_proposal(proposed_location):
    # Registers the proposal, storing the updated number of elves proposing that location
    # Returns TRUE if >1 proposal, False if == 1
    if proposed_location in PROPOSAL_COUNT:
        PROPOSAL_COUNT[proposed_location] += 1
        return True
    else:
        PROPOSAL_COUNT[proposed_location] = 1
        return False

@lru_cache(maxsize=128)
def propose_location(location):
    # Given a location of an elf, choose a proposed new location
    # Iterate to find all possible neighbours
    options = [(location[0] - i + 1,location[1] - j + 1) for j in range(3) for i in range(3)]
    options.remove(location)
    has_neighbour = [loc in ELVES for loc in options] # A list of bools representing if a neighbour is in that location
    # print(location, options, has_neighbour)
    # Check to see if this elf is neighbourless
    if not True in has_neighbour:
        return tuple(location)
    for direction in DIR_DEQUE:
        location_options = DIRECTION_LOCATIONS[direction]
        if not True in [has_neighbour[n] for n in location_options]:
            return tuple(merge(location, DIRECTION_VALUES[direction], "+"))
    # print("There did not seem to a be a neighbourless option")
    return tuple(location)


def find_result():
    min_x, min_y = ELVES[0]
    max_x, max_y = ELVES[0]
    for elf in ELVES:
        min_x = min(min_x, elf[0])
        min_y = min(min_y, elf[1])
        max_x = max(max_x, elf[0])
        max_y = max(max_y, elf[1])
    return min_x, min_y, max_x, max_y

def was_change(test):
    # return True if test matches ELVES
    these_elves = sorted(test, key=lambda x: (x[0], x[1]))
    those_elves = sorted(ELVES, key=lambda x: (x[0], x[1]))
    size = len(these_elves)
    for i in range(size):
        if these_elves[i][1] != those_elves[i][1]:
            return True
    return False


if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    # process incoming
    for j in range(len(data)):
        row = data[j]
        for i in range(len(row)):
            if row[i] == ELF:
                ELVES.append((i,j))
    print(ELVES)
    moved = True
    round = 0
    while moved:
        moved = False
        round += 1
        print(f"Round {round}\nLooking to go {DIR_DEQUE[0]}")
        # Run a round: first come up with a proposal
        for elf in ELVES:
            register_proposal(propose_location(elf))
        # print(PROPOSAL_COUNT)
        # Create a new list of elves, then check to see whose proposal is valid
        new_elves = []
        for elf in ELVES:
            proposal = propose_location(elf)
            if PROPOSAL_COUNT[proposal] == 1:
                new_elves.append(proposal)
            else:
                new_elves.append(elf)
        # Compare elves to new_elves
        moved = was_change(new_elves)
        ELVES = new_elves
        PROPOSAL_COUNT = {}
        DIR_DEQUE.rotate(-1)
        # display_elves()
        # print(PROPOSAL_COUNT)
        # input("Press Enter to continue...")
    min_x, min_y, max_x, max_y = find_result()
    print(min_x, min_y, max_x, max_y)
    print((max_x - min_x + 1) * (max_y - min_y + 1) - len(ELVES))
    print(round)