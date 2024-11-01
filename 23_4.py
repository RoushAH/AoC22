TESTING = True
filename = "data/23_4_sample.txt" if TESTING else "data/23_4.txt"

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()