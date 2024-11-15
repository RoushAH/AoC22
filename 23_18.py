from listfuncs import merge
from utils import get_data

DIRECTION_VALUES = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}
DOWN_PIPES = {"D": "|", "R": "L", "L": "J"}
UP_PIPES = {"U": "|", "R": "F", "L": "7"}
LEFT_PIPES = {"L": "-", "D": "F", "U": "L"}
RIGHT_PIPES = {"R": "-", "U": "J", "D": "7"}
PIPES = {"D": DOWN_PIPES, "U": UP_PIPES, "L": LEFT_PIPES, "R": RIGHT_PIPES}
PIPE_PAIRS = {"7": {"F": False, "L": True}, "J": {"L": False, "F": True}}
DIR_CODES = {"0": "R", "1": "D", "2": "L", "3": "U"}
HEX_VALS = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
dig_cells = set()
wall_cells = {}


def harvest_row(y_value):
    """ When passed a y value, generate the string row corresponding to that y
        This means finding the wall cells involved and padding with '.' values"""
    x_vals = [x[0] for x in wall_cells if x[1] == y_value]
    out_string = " "
    for x in range(min(x_vals), max(x_vals) + 1):
        if (x, y_value) in wall_cells:
            out_string += wall_cells[(x, y_value)]
        else:
            out_string += " "
    out_string += " "
    return out_string


def reconstruct_row(y_value, verticals):
    """ Pass the y-value in question and the set of vertical columns
        Determine how many cells are inside the figure"""

    pass


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
        elif cel in ["7", "J"]:
            if PIPE_PAIRS[cel][last_cross]:
                inside = not inside
        elif cel == "-":
            pass
        elif inside:
            count += 1
    # print("".join(row), count)
    return count


def de_hexify(hex_string):
    hex_string = hex_string[::-1].upper()
    multiplier = 1
    answer = 0
    for char in hex_string:
        if char in HEX_VALS:
            answer += HEX_VALS[char] * multiplier
        else:
            answer += int(char) * multiplier
        multiplier *= 16
    return answer


if __name__ == "__main__":
    stage = 1
    data = get_data(stage, __file__, string=True)
    data = data.split("\n")
    rows = [tuple(x.split()) for x in data]
    rows = [tuple([x[0], int(x[1]), x[2]]) for x in rows]

    # find all cells that have been dug
    steps = []
    loc = (0, 0)
    dig_cells.add(loc)
    for row in rows:
        for step in range(row[1]):
            steps.append(row[0])
            loc = tuple(merge(loc, DIRECTION_VALUES[row[0]], "+"))
            dig_cells.add(loc)

    # find min x, y, max x, y
    xs = set(p[0] for p in dig_cells)
    ys = set(p[1] for p in dig_cells)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    # Iterate over steps, creating the dict of wall_cells
    # min corner so all values are positive
    loc = (0, 0)
    for i, step in enumerate(steps):
        wall_cells[loc] = PIPES[steps[i - 1]][step]
        loc = tuple(merge(loc, DIRECTION_VALUES[step], "+"))

    # iterate over rows from 0 - max_y - min_y
    score = 0
    for row in range(min_y, max_y + 1):
        # print(row, harvest_row(row))
        score += process_row(harvest_row(row))
    print(f"Part 1 score: {score + len(dig_cells)}")

    # Part 2
    corrected_rows = []
    for row in rows:
        new_row = (DIR_CODES[row[2][-2]], de_hexify(row[2][2:-2]))
        corrected_rows.append(new_row)
    dug_cell_count = sum([x[1] for x in corrected_rows])
    loc = (0, 0)
    corners = []
    for row in corrected_rows:
        dir, val = row
        move = (val, val)
        move = tuple(merge(move, DIRECTION_VALUES[dir], "*"))
        loc = tuple(merge(loc, move, "+"))
        corners.append(loc)
    xs = set(p[0] for p in corners)
    ys = set(p[1] for p in corners)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    print(min_x, min_y, max_x, max_y)
    verts = []  # verts stores vertical bars. Stored in the form (x, min_y, max_y)
    for i in range(0, len(corners), 2):
        y_vals = [corners[i][1], corners[i + 1][1]]
        verts.append(tuple([corners[i][0], min(y_vals), max(y_vals)]))
    verts.sort(key=lambda x: x[0])
    print(verts)

    print(f"Part 2 score: {dug_cell_count}")
