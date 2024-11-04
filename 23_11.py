filename = "23_11"
def get_file_name(stage):
    if stage == 0:
        return f"data/{filename}.txt"
    else:
        return f"data/{filename}_sample{stage}.txt"

galaxies = []
empty_rows = []
empty_cols = []

def find_distance(a, b):
    x = abs(a[0] - b[0])
    y = abs(a[1] - b[1])
    # Now I need to check to see if we've passed through some empties
    x_range = (min(a[0], b[0]), max(a[0], b[0]))
    y_range = (min(a[1], b[1]), max(a[1], b[1]))
    for e in empty_rows:
        if y_range[0] < e < y_range[1]:
            y += 1
    for e in empty_cols:
        if x_range[0] < e < x_range[1]:
            x += 1
    return x + y

if __name__ == "__main__":
    stage = 0 # 0 is run
    with open(f"{get_file_name(stage)}", "r") as f:
        data = f.read()
    data = data.split("\n")
    cols = []
    # Find galaxies and empty rows
    for y, line in enumerate(data):
        flag = True
        for x, cel in enumerate(line):
            if cel == "#":
                galaxies.append((x, y))
                flag = False
                cols.append(x)
        if flag:
            empty_rows.append(y)
    for i in range(len(data[0])):
        if i not in cols:
            empty_cols.append(i)
    # Now find each pair and to the job
    score = 0
    for num, gal_a in enumerate(galaxies):
        for gal_b in galaxies[num+1:]:
            score += find_distance(gal_a, gal_b)
    print(f"Part 1 {score}")
