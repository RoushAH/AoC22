from math import sqrt

from utils import ints_in_range

TESTING = False
filename = "data/23_6_sample.txt" if TESTING else "data/23_6.txt"
races = []

def try_race(race):
    time, distance = race[0], race[1]
    # h = time spent still (also equals speed)
    # d = h * (t - h) aka 0 = -h^2 + th - d
    # h = t - sqrt(t^2 - 4d)/ 2 and t + sqrt(t^2 - 4d) / 2
    high = (time + sqrt(time**2 - 4 * distance))/2
    low = (time - sqrt(time**2 - 4 * distance))/2
    print(time, distance, low, high)
    return low, high

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    times = map(lambda x: int(x), data[0].split(":")[1].split())
    distances = map(lambda x: int(x), data[1].split(":")[1].split())
    score = 1
    for time in times:
        races.append((time, next(distances)))
        score *= ints_in_range(*try_race(races[-1]))
    print(f"The score for part 1 is {score}")
    # Part two begins here
    time = int(data[0].split(":")[1].replace(" ",""))
    distance = int(data[1].split(":")[1].replace(" ",""))
    score = ints_in_range(*try_race((time,distance)))
    print(f"The score for part 2 is {score}")