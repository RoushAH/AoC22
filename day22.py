from collections import deque
from listfuncs import merge, compare, rectangularise, rotate

TESTING = True
R = "R"
L = "L"
facing_scores = {"E": 0, "S": 1, "W": 2, "N": 3}
directions = ("E","S","W","N")
turns = {R: -1, L: 1}
OPEN = "."
WALL = "#"
BLANK = " "
map = []
m_width = 0
m_height = 0

filename = "data/day22sample.txt" if TESTING else "data/day22.txt"

def check_space(string):
    count = 0
    for i in range(0, len(string)):
        if string[i] == BLANK:
            count += 1
        else:
            return count
    return count


def harvest_string(value, direction):
    """ Returns the valid component of the string, ignoring blanks, and the count of blanks removed from the beginning"""
    if direction in ["E", "W"]:
        return map[value].strip(), check_space(map[value])
    str_out = ""
    for i in range(m_height):
        str_out += map[i][value]
    return str_out.strip(), check_space(str_out)


def peek(x, y, direction):
    """ Passed, x, y, and direction of character. Returns the next space that character will see """
    if direction in ["E", "W"]:
        active_string, offset = harvest_string(y, direction)
        active_val = x - offset
    else:  # direction in ["N","S"]:
        active_string, offset = harvest_string(x, direction)
        active_val = y - offset
    # Move the active value
    if direction in ["E", "S"]:
        active_val = (1 + active_val) % len(active_string)
        next_char = active_string[active_val]
    else:  # direction in ["W", "N"]:
        active_val = (active_val - 1) % len(active_string)
        next_char = active_string[active_val]
    # put it back together
    if direction in ["E", "W"]:
        x = offset + active_val
    else:  # direction in ["N", "S"]
        y = active_val + offset
    # print(active_val, active_string)
    return next_char, x, y

def new_peek(x, y, direction):
    """ Passed, x, y, and direction of character. Returns the next space that character will see """
    if direction in ["E", "W"]:
        active_string, offset = harvest_string(y, direction)
        active_val = x - offset
    else:  # direction in ["N","S"]:
        active_string, offset = harvest_string(x, direction)
        active_val = y - offset
    # Move the active value IF this move doesn't require a warp
    if direction in ["E", "S"] and active_val + 1 < len(active_string) - 1:
        active_val = 1 + active_val
        next_char = active_string[active_val]
    elif direction in ["W", "N"] and active_val - 1 >= 0:
        active_val = active_val - 1
        next_char = active_string[active_val]
    else:
        # panic
        # Now to do the jump. Here's the dealio -- if I move right, I HAVE to be on a side to my right, right?????
        # So, I need to find somewhere that's right of me. (This could involve warping on the map, annoyingly)
        # I need to reckon the coords in face-centered coords (0-3 for the test-case). If I have to go fewer than 1 face up or down I swap x / y.
        # If I move to the opposite face, I invert the non-active, and maintain the active -- if I'm moving in X I invert y, etc
        pass

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "E"
        self.dirs = deque(["E", "S", "W", "N"])

    def turn(self, turn):
        self.dirs.rotate(turns[turn])
        self.direction = self.dirs[0]

    def move(self, distance):
        # move plan is simple -- for step in distance, see if step is valid.
        # 'peek' at next tile. If next tile is blank, 'peek' does the warping.
        # If next tile is a wall, break. Else, step.
        for step in range(distance):
            next_tile, next_x, next_y = peek(self.x, self.y, self.direction)
            if next_tile == WALL:
                break
            else:
                self.x = next_x
                self.y = next_y

    def move_cube(self, distance):
        # Need a new peek formula
        pass


if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    # ingest data, steps first 'cause they're easier
    steps = data[-1].replace(R, " R ").replace(L, " L ")
    steps = steps.split()
    for i in range(len(steps)):
        if i % 2 == 0:
            steps[i] = int(steps[i])
    print(steps)
    # Find top left starting point
    start = (data[0].find(OPEN), 0)
    you = Character(*start)
    # Set up the global map
    map = data[:-2]
    m_height = len(map)
    rectangularise(map, BLANK)
    m_width = len(map[0])
    # Do the movement
    for step in steps:
        if step in turns:
            you.turn(step)
        else:
            you.move(step)
    print(you.x, you.y, you.direction)
    print(f"Score is {1000 * (you.y + 1) + 4 * (you.x + 1) + facing_scores[you.direction]}")


