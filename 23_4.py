
TESTING = False
filename = "data/23_4_sample.txt" if TESTING else "data/23_4.txt"

def process_game(game_string):
    game_string = game_string[game_string.find(":")+1:]
    game_string = game_string.split("|")
    game_string = [n.strip() for n in game_string]
    first = game_string[0].split()
    second = game_string[1].split()
    first = set([int(n) for n in first])
    second = set(int(n) for n in second)
    return first, second

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    games = [process_game(gm) for gm in data]
    scores = [len(gm[0].intersection(gm[1])) for gm in games]
    score = sum([2**(n-1) for n in scores if n >0])
    print(f"Part 1 score: {score}")
    multipliers = [1 for n in scores]
    # multipliers.insert(0,1)
    for i, game in enumerate(scores):
        print(f"Game {i}: {multipliers[i]}x{game}")
        val = multipliers[i]
        for j in range(1,game+1):
            multipliers[j+i] += val
        print(multipliers)
    print(f"Part 2 score: {sum(multipliers)}")