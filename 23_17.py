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
        return True
    xs = [v.x for v in path[:4]]+[proposed_loc[0]]
    ys = [v.y for v in path[:4]]+[proposed_loc[1]]
    # print(xs, ys)
    return len(ys) > 1 and len(xs) > 1

def cost_path(path: list[Node]):
    cost = sum(l.value for l in path[1:] )
    return cost

def h_cost(path: list[Node]):
    """ Calculate h as cost_path + taxicab distance from last node to finish"""
    last = path[-1]
    taxicab = len(grid)*2 - last.x - last.y - 2
    return taxicab + cost_path(path)

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

def get_neighbour(node, path_so_far):
    x, y = node.x, node.y
    if x > 0 and (grid[y][x-1] not in path_so_far) and legal_proceed(path_so_far, (x - 1, y)):
        yield grid[y][x-1]
    if x < len(grid[0]) - 1 and (grid[y][x+1] not in path_so_far) and legal_proceed(path_so_far, (x + 1, y)):
        yield grid[y][x+1]
    if y > 0 and (grid[y-1][x] not in path_so_far) and legal_proceed(path_so_far, (x, y - 1)):
        yield grid[y-1][x]
    if y < len(grid) - 1 and (grid[y+1][x] not in path_so_far) and legal_proceed(path_so_far, (x, y + 1)):
        yield grid[y+1][x]


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
    print(f"Max bid (diagonal): {max_bid}")
