from functools import reduce

from listfuncs import pad_2d

TESTING = False
filename = "data/23_3_sample.txt" if TESTING else "data/23_3.txt"
data = None
DIGITS = [str(i)for i in range(10)]
GEAR = "*"

def find_number():
    for y in range(len(data)):
        num = ""
        for x in range(len(data[y])):
            if data[y][x] in DIGITS:
                num += data[y][x]
            else:
                if num != "":
                    yield num, x, y
                num = ""

def check_for_symbol(num, x, y):
    length = len(num)
    for j in [y-1, y, y+1]:
        for i in range(x-length-1, x+1):
            if data[j][i] != "." and data[j][i] not in DIGITS:
                return int(num)
    return 0

def check_for_gear(num, x, y):
    length = len(num)
    for j in [y-1, y, y+1]:
        for i in range(x-length-1, x+1):
            if data[j][i] == GEAR:
                return int(num), i, j

def process_gears(gear_list):
    gear_list = list(filter(lambda x: x is not None, gear_list))
    outs = {}
    for gear in gear_list:
        loc = f"{gear[1]:02d}{gear[2]:02d}"
        if loc not in outs:
            outs[loc] = [gear[0], 0]
        else:
            outs[loc][1] = gear[0]
    outs = list(outs.values())
    return sum(list(map(lambda x: x[0]*x[1], outs)))

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    data = [list(row) for row in data]
    data = pad_2d(data, ".")
    answer = 0
    gear_ratios = []
    for num in find_number():
        answer += check_for_symbol(*num)
        gear_ratios.append(check_for_gear(*num))
    gear_ratios = process_gears(gear_ratios)
    print(f"Part 1: {answer}")
    print(f"Part 2: {gear_ratios}")