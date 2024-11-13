# Iterate down the major diagonal to find the minimum bid
# Dijkstra-man! doesn't work. Because best path to spot n+1 != best path to n plus 1
# Need to go back to basic bid, then rando-walk
# Iterate down the major diagonal to find the minimum bid
# Rethink

# Or a priority list of paths attempted? And always operate on the shortest one??
# OoooOooOoooo A* with a heuristic func based on distance to tgt???

from listfuncs import show_2d
from utils import get_data
grid = []
S = "START"
max_bid = 0
diag_walk = []
taxi_weight = 2

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.previous = None

    def __repr__(self):
        if self.previous and self.previous != S:
            return f"({self.x},{self.y}) ${self.value} ({self.previous.x}, {self.previous.y})"
        return f"({self.x},{self.y}) ${self.value}"

def legal_proceed(path:list[Node], proposed_loc):
    if len(path) <= 3: # move at most 3 in the same direction, thus a path of l=3 means no concern is warranted.
        print(f"Short path {path}")
        return True
    xs = set([v.x for v in path[-3:]]+[proposed_loc[0]])
    ys = set([v.y for v in path[-3:]]+[proposed_loc[1]])
    # print(xs, ys)
    min_x = min(xs)
    max_x = max(xs)
    valids = set(range(min_x, max_x+1))
    if valids.difference(xs):
        print(f"Panic! {path} - {proposed_loc}")
    return len(ys) > 1 and len(xs) > 1

def cost_path(path: list[Node]):
    cost = sum(l.value for l in path[1:] )
    return cost

def taxicab(path: list[Node]):
    last = path[-1]
    taxicab = len(grid) * 2 - 2 - last.x - last.y
    return taxicab

def h_cost(path: list[Node]):
    """ Calculate h as cost_path + taxicab distance from last node to finish"""
    path_cost = cost_path(path)
    taxicab_cost = taxicab(path)
    if taxicab_cost * taxi_weight > path_cost:
        taxicab_cost = path_cost * taxi_weight
    return taxicab_cost * taxi_weight + path_cost

def diagonal_bid():
    size = len(grid)
    x, y = 0, 0
    path = []
    while x < size:
        path.append(grid[y][x])
        if y == x:
            x += 1
        else:
            y += 1
    return path

def get_neighbour(path_so_far):
    x, y = path_so_far[-1].x, path_so_far[-1].y
    if x > 0 and (grid[y][x-1] not in path_so_far) and legal_proceed(path_so_far, (x - 1, y)):
        yield grid[y][x-1]
    if x < len(grid[0]) - 1 and (grid[y][x+1] not in path_so_far) and legal_proceed(path_so_far, (x + 1, y)):
        yield grid[y][x+1]
    if y > 0 and (grid[y-1][x] not in path_so_far) and legal_proceed(path_so_far, (x, y - 1)):
        yield grid[y-1][x]
    if y < len(grid) - 1 and (grid[y+1][x] not in path_so_far) and legal_proceed(path_so_far, (x, y + 1)):
        yield grid[y+1][x]


def a_star(start):
    p_queue = [[start]]
    end = grid[len(grid)-1][len(grid)-1]
    end_stage = False
    successes = []
    while p_queue:
        # iteratively add to the first value in p_queue
        path_in_question = p_queue.pop(0)
        # print(f"At {path_in_question[-1]} with cost {h_cost(path_in_question)}")
        for neighbour in get_neighbour(path_in_question):
            p_queue.append(list(path_in_question) + [neighbour])
            if neighbour == end:
                return path_in_question + [neighbour]
        # if end_stage:
        #     successes.sort(key=lambda x: (cost_path(x), len(x)))
        #     p_queue = list(filter(lambda x: h_cost(x) < cost_path(successes[0]), p_queue))
        p_queue.sort(key=lambda x: (-taxicab(x), h_cost(x), cost_path(x)))
        # p_queue = list(filter(lambda x: h_cost(x)/len(x) < max_bid/len(diag_walk), p_queue))
        if len(p_queue) % 100 == 0:
            print(f"Sorted list, {len(p_queue)} paths, best test worth {h_cost(p_queue[0])} with {len(p_queue[0])} steps at {p_queue[0][-1].x},{p_queue[0][-1].y}, worst worth {h_cost(p_queue[-1])} {f'End Stage {cost_path(successes[0])}' if end_stage else ''}")
    return successes


if __name__ == "__main__":
    stage = 1
    data = get_data(stage, __file__, string=True)
    data = data.split("\n")

    super_test = [[1,2,5],[2,7,2],[3,2,1]]
    # data = super_test

    grid = [[Node(i, j, int(data[j][i])) for i in range(len(data[0]))] for j in range(len(data))] # grid of nodes, so we can track la previousa
    grid[0][0].previous = S

    diag_walk = diagonal_bid()
    max_bid = cost_path(diag_walk)
    print(f"Max bid (diagonal): {max_bid} rate of {max_bid / len(diag_walk)}")
    # taxi_weight = max_bid // len(diag_walk)

    path = a_star(grid[0][0])
    print(path)
    print(cost_path(path))