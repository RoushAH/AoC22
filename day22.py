from collections import deque
from listfuncs import merge, compare, rectangularise, rotate, show_2d

TESTING = True
R = "R"
L = "L"
facing_scores = {"E": 0, "S": 1, "W": 2, "N": 3}
directions = ("E", "S", "W", "N")
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
    face_map = [[f"{j // size}{i // size}" if map[j][i]!= BLANK else "  " for i in range(m_width)] for j in range(m_height)]
    # Start by breaking the map into squares of size
    face_names = set([item for sublist in face_map for item in sublist])
    face_names.remove(BLANK+BLANK)
    # Find the various face names, and create Face objects for them
    show_2d(face_map)
    for name in face_names:
        FACES[name] = Face(size)
    for i in range(m_width):
        for j in range(m_height):
            name = face_map[j][i]
            value = map[j][i]
            if name in FACES:
                FACES[name].values[j%size][i%size] = value == OPEN
    # Time to join the faces??
    # Do this first automatically by detecting if number neighbours exist
    for y in range(size):
        for x in range(size):
            # check to see if x, y exists
            if f"{y}{x}" in FACES:
                if f"{y}{(x+1)%size}" in FACES:
                    # There is an east neighbour
                    this_neighbour = f"{(y)%size}{(x+1)%size}"
                    FACES[f"{y}{x}"].neighbours[0] = (this_neighbour, 2)
                    FACES[this_neighbour].neighbours[2] = (f"{y}{x}", 0)
                if f"{(y+1)%size}{x}" in FACES:
                    # There is a south neighbour
                    FACES[f"{y}{x}"].neighbours[1] = (f"{(y+1)%size}{x}", 3)
                    FACES[f"{(y+1)%size}{x}"].neighbours[3] = (f"{y}{x}", 1)
    for k in range(2):
        for orig_face in FACES:
            for direction in [0,1,2,3]: # range(4):
                neighbour = FACES[orig_face].neighbours[direction]
                if neighbour is not None: # we can build off the neighbour
                    # the east neighbour of my north neighbour is my east neighbour, one twist less. Etc.
                    # Need to make sure that this is currently an unknown!
                    tgt = FACES[neighbour[0]] # Harvest the neighbour's name
                    tgt_dir = neighbour[1]
                    new_neighbour = tgt.neighbours[(direction-1)%4] # Find that neighbour's east neighbour
                    if new_neighbour is not None and FACES[orig_face].neighbours[direction-1] is None:
                        print(f"({orig_face}, {direction}), {neighbour}, {new_neighbour}")
                        new_neighbour_edge_num = (new_neighbour[1]+1)%4
                        print(f"This means that the {directions[direction-1]} neighbour of {orig_face} is {(new_neighbour[0], new_neighbour_edge_num)}")
                        FACES[orig_face].neighbours[(direction-1)%4] = (new_neighbour[0], new_neighbour_edge_num)
                        FACES[new_neighbour[0]].neighbours[new_neighbour_edge_num] = (orig_face, (direction+1)%4)
    i = 1
    for orig_face in FACES:
        print(f"Face {orig_face}")
        for direction in range(4):
            neighbour = FACES[orig_face].neighbours[direction]
            if neighbour is not None: # we can build off the neighbour
                print(f"{i}: Face {orig_face}{directions[direction]}{neighbour}")
                i+= 1



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
    process_map(map)
    # Do the movement
    for step in steps:
        if step in turns:
            you.turn(step)
        else:
            you.move(step)
    print(you.x, you.y, you.direction)
    print(f"Score is {1000 * (you.y + 1) + 4 * (you.x + 1) + facing_scores[you.direction]}")
