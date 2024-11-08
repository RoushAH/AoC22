from listfuncs import harvest_string, show_2d
from utils import get_data

results = {}
patterns = []

def find_h_mirror(pattern, try_again=None):
    pattern_height = set(range(len(pattern)))
    answers = []
    for i, row in enumerate(pattern):
        if i + 1 in pattern_height and row == pattern[i + 1]:
            found_flag = True
            k = 1  # iterate k til we run outta road
            while i + 1 + k in pattern_height and i - k in pattern_height:
                if pattern[i + k + 1] != pattern[i - k]:
                    found_flag = False
                k += 1
            if found_flag and not try_again:
                return i + 1
            elif found_flag:
                answers.append(i+1)
    if not try_again:
        return 0
    return answers


def find_v_mirror(pattern, try_again=None):
    answers = []
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
            if found_flag and not try_again:
                return i + 1
            elif found_flag:
                answers.append(i+1)
    if not try_again:
        return 0
    return answers


def process_map(pattern):
    # Given a pattern, try to find a horizontal match. If none exists, try to find a vertical match.
    row = find_h_mirror(pattern)
    col = find_v_mirror(pattern) if row == 0 else 0
    return row, col


def comp_diff(a: list, b: list):
    """ Pass two lists, return a list of true if different else false"""
    if len(a) != len(b):
        return None
    return [a[i] != b[i] for i in range(len(a))]


def desmudge_map(pattern):
    # Pass a pattern. Find possible smudges and see if each returns a valid score.
    # Smudges are possible in a row that a) matches another row but for a single value.
    # This SHOULD BE that a row-smudge creates a row-reflection!
    original = results[str(pattern)]
    options = []
    for i, row_a in enumerate(pattern):
        for j, row_b in enumerate(pattern[i + 1:], i + 1):
            difference = comp_diff(row_a, row_b)
            if difference.count(True) == 1:
                temp_pattern = [list (p) for p in pattern]
                x_pos = difference.index(True)
                temp_pattern[i][x_pos] = temp_pattern[j][x_pos]
                score = find_h_mirror(temp_pattern, try_again=True)
                options.extend([(s,0) for s in score])
                score = find_v_mirror(temp_pattern, try_again=True)
                options.extend([(0,s) for s in score])
    # Assumes a horizontal smudge issue above, vertical below
    for i in range(len(pattern[0])):
        for j in range(i + 1, len(pattern[0])):
            row_a = harvest_string(i, "v", pattern)
            row_b = harvest_string(j, "v", pattern)
            difference = comp_diff(row_a, row_b)
            if difference.count(True) == 1:
                temp_pattern = [list (p) for p in pattern]
                y_pos = difference.index(True)
                temp_pattern[y_pos][i] = temp_pattern[y_pos][j]
                score = find_h_mirror(temp_pattern, try_again=True)
                options.extend([(s,0) for s in score])
                score = find_v_mirror(temp_pattern, try_again=True)
                options.extend([(0,s) for s in score])
    # filter options to only allow legal ones!
    print(f"#{patterns.index(pattern)}: Original:{original}, Options are: {options}")
    options = filter(lambda x: x != original, options)
    answer = set(options)
    if len(answer) ==0:
        num = patterns.index(pattern)
        print(f"Problem on pattern below. In patterns? {pattern in patterns}, #{patterns.index(pattern)}")
        show_2d(pattern)
        print()
        show_2d(patterns[num])
    return answer.pop()


if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__, string=True)
    patterns = data.split("\n\n")
    patterns = [p.split("\n") for p in patterns]
    patterns = [tuple([tuple(list(q)) for q in p]) for p in patterns]
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
    r_score = sum([x[0] for x in scores2])
    c_score = sum([x[1] for x in scores2])
    score = c_score + 100 * r_score
    print(f"Part 2 score: {score}\nValid? {33703 < score}")
