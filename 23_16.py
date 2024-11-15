from manything import Pool

from tqdm import tqdm

from listfuncs import merge, compare
from utils import get_data


DIRECTION_VALUES = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
START = ((0,0),"E")

def moves(cel:str, direction:str):
    """ Take in a cel and a direction of beam travel. Yield further travel(s)
        This is a generator as number of outputs is unknown"""
    if cel == ".":
        yield direction
    elif cel == "\\":
        yield {"E":"S", "N":"W", "W":"N", "S":"E"}[direction]
    elif cel == "/":
        yield {"E":"N","N":"E","W":"S","S":"W"}[direction]
    elif cel == "-":
        if direction in ["E","W"]:
            yield direction
        else:
            for d in ["E","W"]:
                yield d
    elif cel == "|":
        if direction in ["E","W"]:
            for d in ["N","S"]:
                yield d
        else:
            yield direction

def measure_lava(start):
    current_locs = [start]
    visited = set()
    while current_locs:
        current_loc, current_dir = current_locs.pop(0)
        # loop over current stages of the light beam, advancing/bouncing/splitting each one
        visited.add((current_loc, current_dir)) # add the current location to the visited set
        # print(current_loc, current_dir)
        current_cel = data[current_loc[1]][current_loc[0]]
        for move in moves(current_cel, current_dir):
            new_loc = merge(current_loc, DIRECTION_VALUES[move],"+")
            # Need to check to see if it's in-grid before adding
            new_entry = (tuple(new_loc), move)
            if compare(new_loc, (0,0), ">=") and compare(new_loc, (len(data[0]),len(data)), "<") and new_entry not in visited:
                # this "bugs out" as it doesn't allow passthroughs. Perhaps need to keep visited with directionality, too? Then set up a "score-func" to count just the position values?
                current_locs.append(new_entry)

    score_set = set([x[0] for x in visited])
    # print(len(score_set), len(visited))
    return len(score_set)


if __name__ == "__main__":
    stage = 0
    data = get_data(stage, __file__, string=True)
    data = data.split("\n")

    print(f"Part 1 result: {measure_lava(START)}")
    starts = [((0,j),"E") for j in range(0,len(data))] + [((len(data[0])-1,j),"W") for j in range(0,len(data))]
    starts += [((i,0),"S") for i in range(0, len(data[0]))] + [((i, len(data)-1),"N") for i in range(0, len(data))]
    scores = tqdm(map(measure_lava, starts), total=len(starts))
    print(f"Part 2 result: {max(scores)}")
