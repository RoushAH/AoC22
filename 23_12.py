import math
import time
from manything import Pool
import tqdm
from listfuncs import starts_with
from utils import get_file_name, get_data
from math import comb
from functools import lru_cache, cache

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
    if max(short_list + [0]) > max(full_list):
        return False
    if record_so_far.endswith(D):  # and len(short_list) < len(full_list):
        short_list.pop()  # This DOES allow the case of ending with 5 when the max is 3...
    return starts_with(full_list, short_list)


def possibles(record, group_list):
    """ Given a record with Qs and a group list, count the number of possibles """
    # Deliver 6 Qs at a time??? Check the first 6, bin off any invalid options, then continue??
    q_count = 6
    options = [record]

    # Start looping here??
    loops_count = math.ceil(record.count(Q) / q_count)
    for loop in range(loops_count + 1):
        new_options = set()
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
            new_options.update([opt + back_slice for opt in opt_gen if check_start(opt,
                                                                                   group_list)])
        options = new_options
    double_score = len(set(filter(lambda x: get_group_list(x) == list(group_list), options)))
    return double_score, loops_count


def unfold_record(record):
    broken_record, group_list = record[0], record[1]
    full_record = broken_record
    for i in range(4):
        full_record += Q + broken_record
    full_group_list = group_list * 5
    return full_record, full_group_list


def is_valid(record):
    broken_record, group_list = record[0], record[1]
    return (
            group_list[0] <= len(broken_record)
            and
            G not in broken_record[:group_list[0]]
            and (
                    group_list[0] == len(broken_record)
                    or
                    broken_record[group_list[0]] != D
            )
    )


@cache
def recur_check(record):
    broken_record, group_list = record[0], record[1]
    if not group_list:
        return D not in broken_record

    if not broken_record:
        return not group_list

    combos = 0

    if broken_record[0] in [G, Q]:
        # Assume it could be good
        combos += recur_check((broken_record[1:], group_list))

    if broken_record[0] in [D, Q]:
        # Neglect the next group
        if is_valid(record):
            combos += recur_check((broken_record[group_list[0] + 1:], group_list[1:]))

    return combos


def part_2_check(record):
    # Don't think I can discount extras from a Q => G
    broken_record, group_list = record[0], record[1]
    basic_score, blc = possibles(broken_record, group_list)
    double_record = broken_record + Q + broken_record
    double_group_list = group_list * 2

    double_score, loops_count = possibles(double_record, double_group_list)

    chain_score = double_score // basic_score
    p2score = chain_score ** 3 * double_score  # should be chain score!
    return p2score


if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__)
    records = [l.split() for l in data]
    records = [(l[0], l[1].split(",")) for l in records]
    records = [(l[0], tuple([int(i) for i in l[1]])) for l in records]
    start = time.time()
    score, score2 = 0, 0
    p = Pool(3)
    print("Part 1")
    scores = list(tqdm.tqdm(p.map(recur_check, records), total=len(records)))
    print("Part 2")
    records = list(p.map(unfold_record, records))
    scores2 = list(tqdm.tqdm(p.imap_unordered(recur_check, records), total=len(records)))
    score = sum(scores)
    score2 = sum(scores2)
    end = time.time()
    print(f"Score 1: {score}, Valid? {8180 == score}")
    print(
        f"Score 2: {score2}, Valid? {92222689589656 < score2 and score2 not in [358642332799137, 358748438525103]} Test? {score2 == 525152}")
    print(f"Time: {end - start}s")
    # Part 1 -- 19 Qs max
    # Part 2 -- 39 max
