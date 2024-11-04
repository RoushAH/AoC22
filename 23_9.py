TESTING = False
filename = "data/23_9_sample.txt" if TESTING else "data/23_9.txt"

def extrapolate(dataset):
    # if all values are the same, return them
    if len(set(dataset)) == 1:
        return dataset[0]
    # else, generate the difference chart, extrapolate to find the next difference, and apply it
    diffs = []
    for i in range(len(dataset)-1):
        diffs.append(dataset[i+1]-dataset[i])
    diff = extrapolate(diffs)
    return diff + dataset[-1]

def backstrapolate(dataset):
    # if all values are the same, return them
    if len(set(dataset)) == 1:
        return dataset[0]
    # else, generate the difference chart, extrapolate to find the next difference, and apply it
    diffs = []
    for i in range(len(dataset)-1):
        diffs.append(dataset[i+1]-dataset[i])
    diff = backstrapolate(diffs)
    return dataset[0] - diff

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    data = [line.split() for line in data]
    data = [tuple([int(i) for i in line]) for line in data]
    print(data)

    score = 0
    score2 = 0
    for line in data:
        score += extrapolate(line)
        score2 += backstrapolate(line)
    print(f"Part 1 score: {score}")
    print(f"Part 2 score: {score2}")