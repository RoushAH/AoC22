from listfuncs import harvest_string
from utils import get_data

def find_h_mirror(pattern):
    pattern_height = set(range(len(pattern)))
    for i, row in enumerate(pattern):
        if i+1 in pattern_height and row == pattern[i+1]:
            found_flag = True
            k = 1 # iterate k til we run outta road
            while i+1+k in pattern_height and i-k in pattern_height:
                if pattern[i+k+1] != pattern[i-k]:
                    found_flag = False
                k += 1
            if found_flag:
                return i + 1
    return 0

def find_v_mirror(pattern):
    pattern_width = set(range(len(pattern[0])))
    for i in pattern_width:
        if i+1 in pattern_width and harvest_string(i,"v",pattern) == harvest_string(i+1,"v",pattern):
            found_flag = True
            k = 1 # iterate here
            while i+1+k in pattern_width and i-k in pattern_width:
                r = harvest_string(i+1+k,"v",pattern)
                l = harvest_string(i-k,"v",pattern)
                if l != r:
                    found_flag = False
                k += 1
            if found_flag:
                return i + 1
    return 0

def process_map(pattern):
    # Given a pattern, try to find a horizontal match. If none exists, try to find a vertical match.
    row, col = find_h_mirror(pattern), find_v_mirror(pattern)
    return row, col

def desmudge_map(pattern):
    # Pass a pattern. Find possible smudges and see if each returns a valid score.
    # Smudges are possible in a row that a) matches another row but for a single value.
    pass

if __name__ == "__main__":
    stage = 1
    data = get_data(stage=stage, file=__file__, string=True)
    patterns = data.split("\n\n")
    patterns = [p.split("\n") for p in patterns]
    patterns = [[list(q) for q in p] for p in patterns]

    scores = [process_map(pattern) for pattern in patterns]
    r_score = sum([x[0] for x in scores])
    c_score = sum([x[1] for x in scores])
    score = c_score + 100 * r_score
    print(f"Part 1 score: {score}")
    # for i, score in enumerate(scores,1):
    #     print(f"Pattern {i} score: {score}")

    ## Part 2 begins here
    patterns = [[[v == "#" for v in q] for q in p] for p in patterns]