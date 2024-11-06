import math
import time
from multiprocessing import Pool
from turtledemo.penrose import start

from listfuncs import starts_with
from utils import get_file_name, get_data
from math import comb

Q = "?"
D = "#"
G = "."
count = 0


def check_options_old(broken_record, group_list, string_so_far=None):
    # print(f"{broken_record}({len(broken_record)}), {group_list}, {string_so_far}")
    # if len(group_list) == 0, return 1
    if not string_so_far:
        string_so_far = ""
    if not group_list:
        print(f"Found One!{string_so_far} ({len(string_so_far)})")
        return 1
    # Else, come up with possible placements for the 1st group
    this_group = group_list[0]
    remaining_groups = group_list[1:]
    min_length = sum(group_list) + len(group_list) - 1
    group_picture = D * this_group + G
    # remove leading G values
    while broken_record.find(G) == 0:
        broken_record = broken_record[1:]
        group_picture = G + group_picture
    # calculate the minimum length for the groups left, and fail to 0 if this is not available
    if len(broken_record) < min_length:
        print(f"Too short fail{string_so_far}")
        return 0
    result = 0
    # Head must include space for a G after the group of Ds
    head = broken_record[:this_group + 1]
    tail = broken_record[this_group + 1:]
    if head[0] == D:  # if the first one is damaged, we MUST ONLY proceed as damaged
        if len(tail) == 0:
            group_picture = group_picture[:-1]
        return check_options(tail, remaining_groups, string_so_far + group_picture)
    # head[0] == Q. We proceed with the two options
    result = 0
    # If the end of the group is a good, we can proceed as if we've found a complete group
    # print(f"H:{head}, group {this_group}")
    if this_group < len(head) and head[this_group] in [G, Q]:
        result += check_options(tail, remaining_groups, string_so_far + group_picture)
    # also, if the end of the group is a D or a Q, we should try designating the current value as a G
    if this_group < len(head) and head[this_group] in [D, Q]:
        result += check_options(broken_record[1:], group_list, G + string_so_far)
    # Check for 1 Q left at the end...
    if len(head) == this_group and not remaining_groups:
        # print("Found one at the end")
        result += 1
        print(string_so_far + group_picture[:-1])
    return result


def get_group_list(chars_list, Qs_count=None):
    group_list = []
    start_count = 0
    if not Qs_count:
        for char in chars_list:
            if char == D:
                start_count += 1
            elif char in [G, Q]:
                group_list.append(start_count)
                start_count = 0
    else:
        for char in chars_list:
            if char in [D, Q]:
                start_count += 1
            elif char == G:
                group_list.append(start_count)
                start_count = 0

    group_list.append(start_count)
    return list(filter(lambda x: x > 0, group_list))


def bin_gen(length, tgt=None):
    start = [True] * length
    i = 0
    while i < 2 ** length:
        if tgt and start.count(True) == tgt:
            yield start
        else:
            yield start
        i += 1
        val = i
        for pos in range(length):
            start[pos] = val % 2 == 0
            val //= 2


def generate_options(broken_record: str, group_list: list[int] = None):
    # Count the Qs, then generate each possible option
    qs = broken_record.count(Q)
    ds = broken_record.count(D)
    if group_list:
        this_bin = bin_gen(qs, sum(group_list) - ds)
    else:
        this_bin = bin_gen(qs)
    for option in this_bin:
        copy = list(broken_record)
        # Replace Qs based on the recipe given
        for pos in option:
            copy[copy.index(Q)] = D if pos else G
        yield "".join(copy)


def check_options(inp):
    broken_record, group_list = inp[0], inp[1]
    # Create a generator to give all possible combinations for a given record.
    # See how many work
    if max(group_list) < max(get_group_list(broken_record) + [0]) or max(group_list) > max(
            get_group_list(broken_record, Qs_count=True) + [0]):
        # print("A priori fail")
        return 0
    options = generate_options(broken_record, group_list)
    result = 0
    for option in options:
        if get_group_list(option) == list(group_list):
            result += 1
    # print(group_list, result)
    return result


def check_start(record_so_far, full_list):
    """ Given a partial record, see if it MAY match the full list by making sure they start the same.
    Will neglect any trailing block of Ds"""
    short_list = get_group_list(record_so_far)
    if max(short_list+[0]) > max(full_list):
        return False
    if record_so_far.endswith(D):# and len(short_list) < len(full_list):
        short_list.pop()  # This DOES allow the case of ending with 5 when the max is 3...
    return starts_with(full_list, short_list)

def possibles(record, group_list):
    """ Given a record with Qs and a group list, count the number of possibles """
    # Deliver 6 Qs at a time??? Check the first 6, bin off any invalid options, then continue??
    q_count = 4
    options = [record]

    # Start looping here??
    loops_count = math.ceil(record.count(Q) / q_count)
    for loop in range(loops_count + 1):
        new_options = []
        for option in options:
            loc = -1
            for i in range(0, q_count):
                loc = option.find(Q, loc + 1)
                if loc == -1:
                    loc = len(option) - 1
                    break
            record_slice = option[:loc + 1]
            back_slice = option[loc + 1:]
            opt_gen = generate_options(record_slice)
            new_options.extend([opt + back_slice for opt in opt_gen if check_start(opt,
                                                                                   group_list)])
        options = new_options

    double_score = len(list(filter(lambda x: get_group_list(x) == list(group_list), options)))
    return double_score, loops_count


def part_2_check(record):
    # Don't think I can discount extras from a Q => G
    basic_score = check_options(record)
    broken_record, group_list = record[0], record[1]
    # double_record = broken_record + D + broken_record
    double_record = broken_record + Q + broken_record
    double_group_list = group_list * 2

    # double_score, loops_count = possibles(broken_record + D + broken_record, double_group_list)
    double_q_score, loops_count = possibles(double_record, double_group_list)

    # triple_record = double_record + Q + broken_record
    # triple_group_list = group_list * 3
    # triple_score, triple_loops_count = possibles(triple_record, triple_group_list)
    daisy_score = double_q_score // basic_score
    print(f"2x{double_q_score}, Basic {basic_score} Daisy {daisy_score}")
    # Basically, it's 1x basic + between 0 and 4 dasies. Boom, biddy, bye bye
    # n = 4
    # p2score = 0
    # for k in range(n + 1):
    #     coefficient = comb(n, k)
    #     k_score = coefficient * basic_score ** (n - k + 1) * daisy_score ** k
    #     p2score += k_score
    p2score = daisy_score ** 4 * basic_score
    print(f"P2: {p2score}, {record[0]}, Daisy score of {daisy_score}\n")
    # print(f"Or, P2 = {daisy_score ** 4 * basic_score}")
    return p2score


if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__)
    records = [l.split() for l in data]
    records = [(l[0], l[1].split(",")) for l in records]
    records = [(l[0], tuple([int(i) for i in l[1]])) for l in records]
    start = time.time()
    score, score2 = 0, 0
    with Pool(4) as p:
        # scores = p.map(check_options, records)
        scores2 = p.map(part_2_check, records)
    # score = sum(scores)
    score2 = sum(scores2)
    end = time.time()
    # score = 0
    # for n, record in enumerate(records):
    #     record_score = check_options(record)
    #     score += record_score
    # record_2_score = part_2_check(record)
    #     score2 += record_2_score
    #     print(f"{n}: worth {record_score}[1], {record_2_score}[2]")
    print(f"Part 1: {score}, Valid? {8180 == score}")
    print(f"Score 2: {score2}, Valid? {92222689589656 < score2 and 358642332799137 != score2} Test? {score2 == 525152}")
    print(f"Time: {end - start}s")
    # Part 1 -- 19 Qs max
    # Part 2 -- 39 max
