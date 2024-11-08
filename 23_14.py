from listfuncs import harvest_string, flip_2d, show_2d, ends_with, starts_with
from utils import get_data

R = "O"
H = "#"
D = "."

grid = []


def get_score():
    out = []
    for col in range(len(grid[0])):
        column = harvest_string(col, "N", grid)[::-1]  # reverse the column
        col_score = 0
        for i, char in enumerate(column, 1):
            if char == R:
                col_score += i
        out.append(col_score)
    return out


def do_tilt(direction):
    global grid
    size = len(grid) if direction in ["E", "W"] else len(grid[0])
    new_grid = []
    for i in range(size):
        string_in_question = harvest_string(i, direction, grid)  # harvest the right string
        if direction in ["S", "E"]:
            string_in_question = string_in_question[
                                 ::-1]  # Reverse, so things do the Cha Cha slide and ... slide to the left!
        question = list(string_in_question)
        for i in range(len(question)):  # iterate from front to back. If a roller is found, promotify
            if question[i] == R:
                j = i - 1
                while j >= 0 and question[j] == D:
                    question[j], question[j + 1] = question[j + 1], question[j]
                    j -= 1
        # Now reassemble the grid
        string_in_question = "".join(question)
        if direction in ["S", "E"]:
            string_in_question = string_in_question[::-1]  # reverse if required
        # print(string_in_question, direction)

        new_grid.append(string_in_question)

    if direction in ["N", "S"]:
        new_grid = flip_2d(new_grid)
    grid = new_grid


def spin_cycle():
    do_tilt("N")
    do_tilt("W")
    do_tilt("S")
    do_tilt("E")

    return sum(get_score())


if __name__ == "__main__":
    stage = 0

    data = get_data(stage=stage, file=__file__, string=True)
    grid = data.split("\n")

    do_tilt("N")

    score = get_score()
    print(f"Part 1 score: {sum(score)}")

    grid = data.split("\n")
    scores = []
    for i in range(300):
        scores.append(spin_cycle())
        # show_2d(grid)
    # we have a list of score values. There IS a pattern here. We need to now seek this pattern
    # print(scores)
    for pattern_len in range(20, len(scores) // 2):
        pattern_attempt = scores[-pattern_len:]
        remainder = scores[:-pattern_len]
        if ends_with(remainder, pattern_attempt):
            break
    # print(pattern_len, pattern_attempt)
    # find the initial offset
    for offset in range(len(scores)):
        if starts_with(scores[offset:], pattern_attempt):
            break
    # print(f"Offset {offset}")
    # do a minus and a mod
    total = 1000000000
    position = offset + (total - offset) % pattern_len
    # print(f"Position {position}")
    answer = scores[position-1]
    guesses = [95243, 95282, 95370, 95198, 95198, 95324, 95493, 95320, 95285]
    print(f"Value: {answer} Valid? {95198 < answer < 95370 and answer not in guesses}")
    # print(scores[position-2:position+2])
    # print([ans for ans in pattern_attempt if ans not in guesses])
