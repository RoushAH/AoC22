from collections import deque

from listfuncs import merge

filename = "23_10"
map = []
STARTER = "S"
DIRECTION_VALUES = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
DIR_DEQUE = deque(["N", "E", "S", "W"])
PIPES = {"|": ["N", "S"], "-": ["E", "W"], "L": ["N", "E"], "J": ["N", "W"], "7": ["S", "W"], "F": ["S", "E"]}
for pipe in PIPES:
    PIPES[pipe].sort()
history = []
PIPE_PAIRS = {"7": {"F": False, "L": True}, "J":{"L":False, "F":True}}


def next_spot(x, y, dir):
    """ Take in a coordinate and a direction. Return the same for the next step"""
    direction_in_next = DIR_DEQUE[DIR_DEQUE.index(dir)-2] # Find the direction FROM which I will enter the NEXT cell
    new_x,new_y = merge(DIRECTION_VALUES[dir], (x,y), "+")
    next_pipe = map[new_y][new_x]
    if next_pipe == STARTER:
        return new_x, new_y, "", next_pipe
    direction_out_next = PIPES[next_pipe][PIPES[next_pipe].index(direction_in_next) - 1]
    return new_x, new_y, direction_out_next, next_pipe

def find_start():
    """ Find the starting spot. Return x, y, direction to start in, and a dummy next_pipe value"""
    x, y = -1, -1
    for j, row in enumerate(map):
        if STARTER in row:
            y = j
            x = row.index(STARTER)
    replacement_dirs = []
    for direction in DIR_DEQUE:
        opposite = DIR_DEQUE[DIR_DEQUE.index(direction)-2]
        temp_x, temp_y = merge(DIRECTION_VALUES[opposite], (x,y), "+") # If "direction" is N, this means we are searching for something we can ENTER from N
        neighbour = map[temp_y][temp_x]
        if neighbour in PIPES and direction in PIPES[neighbour]:
            dir_out = opposite
            replacement_dirs.append(opposite)
    return x, y, dir_out, "next_pipe", replacement_dirs

def get_file_name(stage):
    if stage == 0:
        return f"data/{filename}.txt"
    else:
        return f"data/{filename}_sample{stage}.txt"

def process_row(row_in_question):
    inside = False
    count = 0
    last_cross = ""
    for cel in row_in_question:
        # if I start with F and end with 7, I am outside. if I start with F and end with J, I am inside
        if cel == "|":
            inside = not inside
        elif cel in ["F", "L"]:
            last_cross = cel
        elif cel in ["7","J"]:
            if PIPE_PAIRS[cel][last_cross]:
                inside = not inside
        elif cel == "-":
            pass
        elif inside:
            count += 1
    # print("".join(row), count)
    return count

def clean_map():
    for y in range(len(map)):
        for x in range(len(map[0])):
            if (x,y) not in history:
                map[y][x] = "."

if __name__ == "__main__":
    stage = 0 # 0 is run
    with open(f"{get_file_name(stage)}", "r") as f:
        data = f.read()
    data = data.split("\n")
    map = [list(line) for line in data]
    steps = 0
    x, y, direction, next_pipe, replacement = find_start()

    while next_pipe != STARTER:
        x, y, direction, next_pipe = next_spot(x, y, direction)
        history.append((x,y))
        steps += 1
    print(f"Part 1 score {steps/2}")

    # Fix the starter so we can do a crossing game!
    x, y, direction, next_pipe, replacement = find_start()
    replacement.sort()
    for pipe in PIPES:
        if len(set(PIPES[pipe]).difference(set(replacement))) == 0 :
            map[y][x] = pipe
            print(f"{x},{y} is now {pipe}")

    # Do the crossing game! Read across each row L -> R
    clean_map()
    score = 0
    for row in map:
        score += process_row(row)
    print(f"Part 2 score {score}")
