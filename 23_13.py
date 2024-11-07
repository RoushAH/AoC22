from listfuncs import harvest_string, show_2d
from utils import get_data

results = {}


def find_h_mirror(pattern, try_again=None):
    pattern_height = set(range(len(pattern)))
    no_go = 0 or try_again
    for i, row in enumerate(pattern):
        if i + 1 in pattern_height and row == pattern[i + 1]:
            found_flag = True
            k = 1  # iterate k til we run outta road
            while i + 1 + k in pattern_height and i - k in pattern_height:
                if pattern[i + k + 1] != pattern[i - k]:
                    found_flag = False
                k += 1
            if found_flag and i+1 != no_go:
                return i + 1
    return 0


def find_v_mirror(pattern, try_again=None):
    no_go = 0 or try_again
    pattern_width = set(range(len(pattern[0])))
    for i in pattern_width:
        if i + 1 in pattern_width and harvest_string(i, "v", pattern) == harvest_string(i + 1, "v", pattern):
            found_flag = True
            k = 1  # iterate here
            while i + 1 + k in pattern_width and i - k in pattern_width:
                r = harvest_string(i + 1 + k, "v", pattern)
                l = harvest_string(i - k, "v", pattern)
                if l != r:
                    found_flag = False
                k += 1
            if found_flag and i+1 != no_go:
                return i + 1
    return 0


def process_map(pattern, try_again=None):
    # Given a pattern, try to find a horizontal match. If none exists, try to find a vertical match.
    row = find_h_mirror(pattern, try_again)
    col = find_v_mirror(pattern, try_again) if row == 0 else 0
    return row, col


def comp_diff(a: list, b: list):
    """ Pass two lists, return a list of true if different else false"""
    if len(a) != len(b):
        return None
    return [a[i] != b[i] for i in range(len(a))]


def desmudge_map(pattern):
    # Pass a pattern. Find possible smudges and see if each returns a valid score.
    # Smudges are possible in a row that a) matches another row but for a single value.
    original = results[str(pattern)]
    for i, row_a in enumerate(pattern):
        for j, row_b in enumerate(pattern[i + 1:], i + 1):
            difference = comp_diff(row_a, row_b)
            if difference.count(True) == 1:
                temp_pattern = pattern.copy()
                x_pos = difference.index(True)
                temp_pattern[i][x_pos] = temp_pattern[j][x_pos]
                score = process_map(temp_pattern, original[0])
                if score not in [ (0, 0) , original]:
                    return score
    # Assumes a horizontal smudge issue above, vertical below
    for i in range(len(pattern[0])):
        for j in range(i + 1, len(pattern[0])):
            row_a = harvest_string(i, "v", pattern)
            row_b = harvest_string(j, "v", pattern)
            difference = comp_diff(row_a, row_b)
            if difference.count(True) == 1:
                temp_pattern = pattern.copy()
                y_pos = difference.index(True)
                temp_pattern[y_pos][i] = temp_pattern[y_pos][j]
                score = process_map(temp_pattern, original[1])
                if score not in [ (0, 0) , original]:
                    return score
    return None


if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__, string=True)
    patterns = data.split("\n\n")
    patterns = [p.split("\n") for p in patterns]
    patterns = [[list(q) for q in p] for p in patterns]
    print(f"There are {len(patterns)} patterns to solve")

    results = {str(pattern): process_map(pattern) for pattern in patterns}
    scores = results.values()
    r_score = sum([x[0] for x in scores])
    c_score = sum([x[1] for x in scores])
    score = c_score + 100 * r_score
    print(f"Part 1 score: {score}")

    ## Part 2 begins here
    # Need to ensure that this is different to the original
    scores2 = [desmudge_map(pattern) for pattern in patterns]
    print(f"{comp_diff(list(scores), scores2).count(False)} results matching from the first round, {scores2.count(None)} Nones")
    print(scores2)
    r_score = sum([x[0] for x in scores2])
    c_score = sum([x[1] for x in scores2])
    score = c_score + 100 * r_score
    print(f"Part 2 score: {score}\nValid? {33703 < score}")
