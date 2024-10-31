from listfuncs import compare

TESTING = False
filename = "data/23_1_sample.txt" if TESTING else "data/23_1.txt"
# Storing things as tuples R,G,B
GAME_MAX = (12,13,14)
NAMES = ("red","green","blue")

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    # Store a dict of games, game_id:list[tuple[r,g,b]]