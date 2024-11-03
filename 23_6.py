TESTING = True
filename = "data/23_6_sample.txt" if TESTING else "data/23_6.txt"
races = []

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    times = map(lambda x: int(x), data[0].split(":")[1].split())
    distances = map(lambda x: int(x), data[1].split(":")[1].split())
    for time in times:
        races.append((time, next(distances)))
    # print(races)