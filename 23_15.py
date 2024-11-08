from utils import get_data

class Lens:
    def __init__(self, name, focal):
        self.focal = int(focal)
        self.name = name

    def __str__(self):
        return f"{self.name} {self.focal}"

def HASH(string):
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256
    return val

def HASHMAP_box(box: list[Lens], string):
    box_names = [b.name for b in box]
    if string[-1] == "-": # remove the set lens
        string = string[:-1]
        if string in box_names:
            box.pop(box_names.index(string))
    elif "=" in string: # Modify the set lens
        lens_name = string[:string.index("=")]
        lens_focal = string[string.index("=")+1:]
        if lens_name in box_names:
            box[box_names.index(lens_name)].focal = int(lens_focal)
        else:
            box.append(Lens(lens_name, lens_focal))
    return box

def split_command(string):
    if "-" in string:
        return string.split("-")[0], None
    elif "=" in string: # Modify the set lens
        lens_name = string[:string.index("=")]
        lens_focal = string[string.index("=")+1:]
        return lens_name, lens_focal
    else:
        return string, None

def do_box_score(box):
    box_score = 0
    for pos, lens in enumerate(box,1):
        box_score += pos * lens.focal
    return box_score

if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__, string=True)
    data = data.split(",")

    score = 0
    for string in data:
        res = HASH(string)
        score += res
        print(f"{string} => {res}")
    print(f"Part 1 score: {score}")

    boxen = [[] for _ in range(256)]
    for string in data:
        name, value = split_command(string)
        res = HASH(name)
        boxen[res] = HASHMAP_box(boxen[res], string)
        print(f"{string} \n")
        for i in range(len(boxen)):
            if len(boxen[i]) > 0:
                print(f"Box {i}:")
                for lens in boxen[i]:
                    print(f"\t{lens}")
        print("\n\n")

    score = 0
    for boxnum, box in enumerate(boxen, 1):
        score += do_box_score(box) * boxnum
    print(f"Part 2 score: {score}")