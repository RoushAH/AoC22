# Iterate down the major diagonal to find the minimum bid
# Dijkstra-man! doesn't work. Because best path to spot n+1 != best path to n plus 1
# Need to go back to basic bid, then rando-walk
# Iterate down the major diagonal to find the minimum bid
# Rethink

# Or a priority list of paths attempted? And always operate on the shortest one??
# OoooOooOoooo A* with a heuristic func based on distance to tgt???

from utils import get_data
grid = []
S = "START"
taxi_weight = 1

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.previous = None
        self.total_cost = None
        self.visited = False

    def __repr__(self):
        if self.previous and self.previous != S:
            return f"({self.x},{self.y}) ${self.value}"
        return f"({self.x},{self.y}) ${self.value}"

def legal_proceed(loc_a: Node, loc_b: tuple[int]):
    x, y = loc_a.x, loc_a.y
    loc_b = grid[loc_b[1]][loc_b[0]]
    hist = [loc_b, loc_a]
    # get the loc b for history thing then iterate
    for i in range(3):
        prev = grid[y][x].previous
        if not prev:
            print(f"No previous for ({x},{y}) in {hist}")
            return True
        hist.append(prev)
        x, y = prev.x, prev.y
    xs = set([v.x for v in hist])
    ys = set(v.y for v in hist)
    # print(hist, xs, ys)
    return len(ys) > 1 and len(xs) > 1

def reconstruct_path(end_node: Node):
    so_far = [end_node]
    current = so_far[0]
    while current.previous:
        current = current.previous
        so_far.append(current)
    so_far.reverse()
    return so_far

def cost_path(path: list[Node]):
    cost = sum(l.value for l in path[1:] )
    return cost

def taxicab(last: Node):
    taxicab_cost = abs(len(grid) - 1 - last.x) + abs(len(grid) - 1 - last.y)
    return taxicab_cost

def f_cost(last: Node):
    """ Calculate h as cost_path + taxicab distance from last node to finish"""
    path_cost = last.total_cost
    taxicab_cost = taxicab(last)
    # if taxicab_cost * taxi_weight > path_cost:
    #     taxicab_cost = path_cost * taxi_weight
    return taxicab_cost * taxi_weight + path_cost

def get_neighbors(node: Node):
    x, y = node.x, node.y
    if x > 0 and not grid[y][x-1].visited and legal_proceed(node, (x-1, y)):
        yield grid[y][x-1]
    if x < len(grid[0]) - 1 and not grid[y][x+1].visited and legal_proceed(node, (x+1, y)):
        yield grid[y][x+1]
    if y > 0 and not grid[y-1][x].visited and legal_proceed(node, (x, y-1)):
        yield grid[y-1][x]
    if y < len(grid) - 1 and not grid[y+1][x].visited and legal_proceed(node, (x, y+1)):
        yield grid[y+1][x]

def a_star(start, goal):
    """ A* algorithm. Using n.total_cost to store the f-cost then cost when visited,
        visited = True when visited"""
    open_set = [start] # priority queue, ordered by cost from start. This can be done by ordering by x.total_cost
    # came_from stored as n.previous
    start.total_cost = 0
    while open_set:
        current = open_set.pop(0)
        current.visited = True
        print(current)
        if current == goal:
            return current
        for neighbor in get_neighbors(current):
            # do the thing
            tentative_cost = current.total_cost + neighbor.value
            if not neighbor.total_cost or tentative_cost < neighbor.total_cost: # We need to update IF the cost is none, or we've got a better cost
                neighbor.total_cost = tentative_cost
                neighbor.previous = current
                if neighbor not in open_set:
                    open_set.append(neighbor)
        open_set.sort(key=lambda n: f_cost(n))

def visualize_path(grid, path):
    for j in range(len(grid)):
        row = ""
        for i in range(len(grid[j])):
            if grid[j][i] in path:
                row += "#"
            else:
                row += "."
        print(row)


if __name__ == "__main__":
    stage = 1
    data = get_data(stage, __file__, string=True)
    data = data.split("\n")

    super_test = [[1,2,5],[2,7,2],[3,2,1]]
    # data = super_test

    grid = [[Node(i, j, int(data[j][i])) for i in range(len(data[0]))] for j in range(len(data))] # grid of nodes, so we can track la previousa
    start = grid[0][0]
    finish = grid[len(data) - 1][len(data) - 1]
    start, finish = finish, start

    a_star(start, finish)
    print(finish.total_cost)
    path = reconstruct_path(finish)
    path.reverse()
    print(path)
    print(cost_path(path))
    visualize_path(grid, path)