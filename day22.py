from collections import deque
from zipfile import sizeEndCentDir

from listfuncs import merge, compare, rectangularise, rotate, show_2d

TESTING = True
R = "R"
L = "L"
facing_scores = {"E": 0, "S": 1, "W": 2, "N": 3}
directions = ("E", "S", "W", "N")
direction_moves = {"E": (1, 0), "S": (0, 1), "W": (-1, 0), "N": (0, -1)}
turns = {R: -1, L: 1}
OPEN = "."
WALL = "#"
BLANK = " "
map = []
m_width = 0
m_height = 0
FACES = {}

filename = "data/day22sample.txt" if TESTING else "data/day22.txt"


class Face:
    def __init__(self, size):
        self.size = size
        self.values = [[False for i in range(size)] for j in range(size)]
        self.orientation = deque(directions)
        # sides in order east, south, west, north,
        # stored as a tuple of (face_num, bordering side)
        self.neighbours = [None, None, None, None]

    def rotate(self, direction):
        if direction < 0:
            direction = -1
        elif direction > 0:
            direction = 1
        self.values = rotate(self.values, direction)
        self.orientation.rotate(direction)

    def orient(self):
        turns = 0
        while self.orientation[0] != "E":
            self.rotate(-1)
            turns += 1
        return turns

    def __str__(self):
        output = ""
        for i in range(len(self.values)):
            for j in range(len(self.values[i])):
                if self.values[i][j]:
                    output += OPEN
                else:
                    output += WALL
            output += "\n"
        output += " ".join(self.neighbours)
        return output


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


def new_peek(face, x, y, direction):
    """ Passed, x, y, and direction of character.
    Returns the next space that character will see, the face, x, y coords, and the facing direction """
    new_coord = merge((x, y), direction_moves[direction], "+")
    this_face = FACES[face]
    size = this_face.size
    # First, check to see if we will not need to warp, and return the easy answer
    if compare(new_coord, (0, 0), ">=") and compare(new_coord, (size, size), "<"):
        x = new_coord[0]
        y = new_coord[1]
        return this_face.values[y][x], face, x, y, direction
    # Next, let's look at moving from one edge to another
    edge_from = facing_scores[direction]
    face_to, edge_to = this_face.neighbours[edge_from]
    offset = (edge_to - edge_from) % 4
    new_face = FACES[face_to]
    # The four cases based on how much we rotate, starting with a straight map connection -- W->E, etc
    # print(f"Offset = {offset}")
    if abs(offset) == 2:
        new_coord = merge(new_coord, (size, size), "%")
        x = new_coord[0]
        y = new_coord[1]
    elif offset == 0:
        # This a scary -- this one means my north is their north, etc.
        # What ends up happening is that for N, S, the y value is the same, the x value reflects x = (size-1)-x
        # Flip the direction 180 degrees, or pi radians
        if direction in ["E", "W"]:
            y = size - 1 - y
        elif direction in ["S", "N"]:
            x = size - 1 - x
        direction = directions[directions.index(direction) - 2]
    elif offset == 1:  # W -> N, etc
        # this is the scariest to me. there's some swapping thing going on...
        x, y = y, x
        if edge_to == 0:
            x = size - 1
        elif edge_to == 1:
            y = size - 1
        elif edge_to == 2:
            x = 0
        elif edge_to == 3:
            y = 0
        direction = directions[directions.index(direction) - offset]
    elif offset == 3:
        # swap and subtract
        if edge_to == 0:
            y = size - 1 - x
            x = size - 1
        elif edge_to == 1:
            x = size - 1 - y
            y = size - 1
        elif edge_to == 2:
            y = size - 1 - x
            x = 0
        elif edge_to == 3:
            x = size - 1 - y
            y = 0
        direction = directions[directions.index(direction) - offset]
    return new_face.values[y][x], face_to, x, y, direction


class Character:
    def __init__(self, x, y, face=None):
        self.x = x
        self.y = y
        self.direction = "E"
        self.face = face
        self.dirs = deque(["E", "S", "W", "N"])

    def turn(self, turn):
        self.dirs.rotate(turns[turn])
        self.direction = self.dirs[0]

    def turn_to_face(self, final_direction):
        while self.direction != final_direction:
            self.turn("L")

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


def process_map(map):
    # Break the map into numbered faces of non-blank values
    # Then ask the user to group them?
    # Detect the size
    size = len(map[0])
    for row in range(len(map)):
        data, offset = harvest_string(row, "E")
        size = min(len(data), size)
    global FACES
    face_map = map.copy()
    # replace with TRUE or FALSE
    face_map = [[f"{j // size}{i // size}" if map[j][i] != BLANK else "  " for i in range(m_width)] for j in
                range(m_height)]
    # Start by breaking the map into squares of size
    face_names = set([item for sublist in face_map for item in sublist])
    face_names.remove(BLANK + BLANK)
    # Find the various face names, and create Face objects for them
    show_2d(face_map)
    for name in face_names:
        FACES[name] = Face(size)
    for i in range(m_width):
        for j in range(m_height):
            name = face_map[j][i]
            value = map[j][i]
            if name in FACES:
                FACES[name].values[j % size][i % size] = value == OPEN
    # Time to join the faces??
    # Do this first automatically by detecting if number neighbours exist
    for y in range(size):
        for x in range(size):
            # check to see if x, y exists
            if f"{y}{x}" in FACES:
                if f"{y}{(x + 1) % size}" in FACES:
                    # There is an east neighbour
                    this_neighbour = f"{(y) % size}{(x + 1) % size}"
                    FACES[f"{y}{x}"].neighbours[0] = (this_neighbour, 2)
                    FACES[this_neighbour].neighbours[2] = (f"{y}{x}", 0)
                if f"{(y + 1) % size}{x}" in FACES:
                    # There is a south neighbour
                    FACES[f"{y}{x}"].neighbours[1] = (f"{(y + 1) % size}{x}", 3)
                    FACES[f"{(y + 1) % size}{x}"].neighbours[3] = (f"{y}{x}", 1)
    for orig_face in FACES:
        # - if I go to a neighbour i share side l = > n with
        # -   go to his neighbour n + 1 = > m
        # -   my l - 1 = > m + 1
        for l in range(4):
            neighbour = FACES[orig_face].neighbours[l]
            if neighbour is not None:  # we can build off the neighbour
                # Need to make sure that this is currently an unknown!
                known_neighbour = FACES[neighbour[0]]  # Harvest the neighbour object from the name
                n = neighbour[1]
                for offset in [-1, 1]:  # this is the number of steps EASTWARD to compare NEEDS TO BE in[-1, 1]
                    new_neighbour = known_neighbour.neighbours[
                        (n + offset) % 4]  # Find that neighbour's neighbour one twist eastward
                    if new_neighbour is not None and FACES[orig_face].neighbours[(l - offset) % 4] is None:
                        m = new_neighbour[1]
                        # print(f"Off by {offset} ({orig_face}, {l}), {neighbour}, {new_neighbour}")
                        # print(
                        #     f"This means that the {directions[(l - offset) % 4]} neighbour of {orig_face} is {(new_neighbour[0], directions[(m + offset) % 4])}")
                        FACES[orig_face].neighbours[(l - offset) % 4] = (new_neighbour[0], (m + offset) % 4)
                        FACES[new_neighbour[0]].neighbours[(m + offset) % 4] = (orig_face, (l - offset) % 4)
    # i = 1
    # for orig_face in FACES:
    #     print(f"Face {orig_face}")
    #     for orig_direction in range(4):
    #         neighbour = FACES[orig_face].neighbours[orig_direction]
    #         if neighbour is not None:  # we can build off the neighbour
    #             print(f"{i}: Face {orig_face}{directions[orig_direction]}{neighbour}")
    #             i += 1
    return "0" + str(min([int(nom) for nom in FACES]))


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
    start_face = process_map(map)
    # Do the movement
    for step in steps:
        if step in turns:
            you.turn(step)
        else:
            you.move(step)
    print("Phase 1")
    print(you.x, you.y, you.direction)
    print(f"Score is {1000 * (you.y + 1) + 4 * (you.x + 1) + facing_scores[you.direction]}")

    print(start_face)
    me = Character(0, 0, start_face)
    print(me.x, me.y, me.direction, me.face)
    print(new_peek("11", 1, 3, "S"))
