from multiprocessing import Pool

from utils import get_file_name, get_data
from math import log2
Q = "?"
D = "#"
G = "."

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
    group_picture = D*this_group+G
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
    head = broken_record[:this_group+1]
    tail = broken_record[this_group+1:]
    if head[0] == D: # if the first one is damaged, we MUST ONLY proceed as damaged
        if len(tail) == 0:
            group_picture = group_picture[:-1]
        return check_options(tail, remaining_groups, string_so_far+group_picture)
    # head[0] == Q. We proceed with the two options
    result = 0
    # If the end of the group is a good, we can proceed as if we've found a complete group
    # print(f"H:{head}, group {this_group}")
    if this_group < len(head) and head[this_group] in [G, Q]:
        result += check_options(tail, remaining_groups, string_so_far+group_picture)
    # also, if the end of the group is a D or a Q, we should try designating the current value as a G
    if this_group < len(head) and head[this_group] in [D, Q]:
        result += check_options(broken_record[1:], group_list, G+string_so_far)
    # Check for 1 Q left at the end...
    if len(head) == this_group and not remaining_groups:
        # print("Found one at the end")
        result += 1
        print(string_so_far+group_picture[:-1])
    return result

def get_group_list(chars_list):
    group_list = []
    start_count = 0
    for char in chars_list:
        if char == D:
            start_count += 1
        elif char == G:
            group_list.append(start_count)
            start_count = 0
    group_list.append(start_count)
    return list(filter(lambda x: x> 0,group_list))

def bin_gen(length, tgt=None):
    start = [True]*length
    i = 0
    while i < 2**length:
        if tgt and start.count(True) == tgt:
            yield start
        else:
            yield start
        i += 1
        val = i
        for pos in range(length):
            start[pos] = val % 2 == 0
            val //= 2

def generate_options(broken_record:str, group_list:list[int]):
    # Count the Qs, then generate each possible option
    qs = broken_record.count(Q)
    ds = broken_record.count(D)
    bin = bin_gen(qs, sum(group_list)-ds)
    for option in bin:
        copy = list(broken_record)
        # Replace Qs based on the recipe given
        for pos in option:
            copy[copy.index(Q)] = D if pos else G
        yield "".join(copy)


def check_options(inp):
    broken_record, group_list = inp[0], inp[1]
    # Create a generator to give all possible combinations for a given record.
    # See how many work
    options = generate_options(broken_record, group_list)
    result = 0
    for option in options:
        if get_group_list(option) == list(group_list):
            result += 1
    # print(group_list, result)
    return result

def unfold(record):
    broken_record, group_list = record[0], record[1]
    new_record_string = broken_record+Q+broken_record+Q+broken_record+Q+broken_record+Q+broken_record
    new_group_list = group_list*5
    return new_record_string, new_group_list

def triple_check(record):
    broken_record, group_list = record[0], record[1]
    basic_score = check_options(record)
    add_to_front_score = check_options((Q+broken_record,group_list))
    add_to_end_score = check_options((broken_record+Q, group_list))
    score = basic_score * add_to_front_score ** 4 + add_to_end_score ** 4 * basic_score
    print(basic_score, add_to_front_score, add_to_end_score, score)
    return score

if __name__ == "__main__":
    stage = 1
    data = get_data(stage=stage, file=__file__)
    records = [l.split() for l in data]
    records = [(l[0], l[1].split(",")) for l in records]
    records = [(l[0], tuple([int(i) for i in l[1]])) for l in records]
    score, score2 = 0, 0
    # with Pool(8) as p:
    #     scores = p.map(check_options, records)
    # score = sum(scores)
    for n, record in enumerate(records):
        record_score = check_options(record)
        print(f"{n}: {record} ({record[0].count(Q)}) worth {record_score}")
        score += record_score
        score2 += triple_check(record)
        print(f"Score 2 = {score2}")
    print(f"Part 1: {score}, Valid? {8314 > score}")
