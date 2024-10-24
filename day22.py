TESTING = True
R = "R"
L = "L"

filename = "day22sample.txt" if TESTING else "day22.txt"

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.readlines()
    # ingest data, steps first 'cause they're easier
    steps = data[-1].replace(R, " R ").replace(L, " L ")
    steps = steps.split()

    print(steps)