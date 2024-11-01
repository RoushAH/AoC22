from functools import reduce

TESTING = False
filename = "data/23_2_sample.txt" if TESTING else "data/23_2.txt"
# Storing things as tuples R,G,B
GAME_MAX = (12,13,14)
NAMES = ("red","green","blue")

def find_power(game_string):
    plays = game_string.split(";")
    mins = {name: 0 for name in NAMES}
    for play in plays:
        results = play.split(",")
        for result in results:
            this_result = result.strip().split(" ")
            mins[this_result[1]] = max(int(this_result[0]), mins[this_result[1]])
    return reduce((lambda x, y: x * y), mins.values())

def package_game(game_string):
    plays = game_string.split(";")
    for play in plays:
        results = play.split(",")
        for result in results:
            for i in range(len(NAMES)):
                if NAMES[i] in result:
                    rolls = int(result.split()[0])
                    if rolls > GAME_MAX[i]:
                        return False
    return True

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    # Store a list of games, list[bool]
    games = [False]
    part_2 = 0
    for game in data:
        game = game.split(":")[1]
        games.append(package_game(game))
        part_2 += find_power(game)
    result = sum([i for i in range(len(games)) if games[i]])
    print(f"Part 1: {result}")
    print(f"Part 2: {part_2}")
