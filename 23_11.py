filename = "23_11"
def get_file_name(stage):
    if stage == 0:
        return f"data/{filename}.txt"
    else:
        return f"data/{filename}_sample{stage}.txt"

galaxies = []
empty_rows = []
empty_cols = []

if __name__ == "__main__":
    stage = 1 # 0 is run
    with open(f"{get_file_name(stage)}", "r") as f:
        data = f.read()
    data = data.split("\n")
    print(data)
    # Find galaxies and empty rows
    for y, line in enumerate(data):
        flag = True
        for x, cel in enumerate(line):
            if cel == "#":
                galaxies.append((x, y))
                flag = False
        if flag:
            empty_rows.append(y)
    print(galaxies)
    print(empty_rows)
