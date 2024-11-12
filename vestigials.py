from collections import deque
from day22 import facing_scores, OPEN, BLANK, WALL
from listfuncs import rotate

class Cube:
    def __init__(self, size):
        self.size = size
        self.sides = {i:Face(size) for i in range(1,7)}
        self.sides[1].neighbours = deque([3,2,4,5])
        self.sides[2].neighbours = deque([3,6,4,1])
        self.sides[3].neighbours = deque([6,2,1,5])
        self.sides[4].neighbours = deque([1,2,6,5])
        self.sides[5].neighbours = deque([3,1,4,6])
        self.sides[6].neighbours = deque([4,5,3,2]) # side 6 is upside-down to the user!
        self.facing = 1

    def rotate(self, direction):
        # rotate the two pivoting faces, then change the facing side
        direction_int = facing_scores[direction]
        current = self.sides[self.facing]
        self.sides[current.neighbours[direction_int-1]].rotate(1)
        self.sides[current.neighbours[(direction_int+1)%4]].rotate(-1)
        self.facing = current.neighbours[direction_int]

    def __str__(self):
        output = ""
        for i in range(len(self.sides)):
            output += f"\n\nSide {i+1}\n"
            output += self.sides[i+1].__str__()
        output += f"\n\nFacing side {self.facing}\n"
        return output

def legal_proceed(loc_a, loc_b):
    x, y = loc_b
    hist = [loc_a, loc_b]
    # get the loc b for history thing
    prev = grid[y][x].previous
    if prev == "START":
        print(f"No previous for {loc_a}=>{x},{y}")
        return True
    hist.append((prev.x, prev.y))
    prev2 = grid[prev.y][prev.x].previous
    if prev2 == "START":
        print(f"No previous for {loc_a}=>{loc_b}=>{prev.x},{prev.y}")
        return True
    hist.append((prev2.x, prev2.y))
    xs = set([v[0] for v in hist])
    ys = set(v[1] for v in hist)
    # print(hist, xs, ys)
    return len(ys) > 1 and len(xs) > 1

def get_neighbour(x, y, visited=None):
    if x > 0 and not grid[y][x-1].previous and legal_proceed((x-1, y),(x,y)):
        yield grid[y][x-1]
    if x < len(grid[0]) - 1 and not grid[y][x+1].previous and legal_proceed((x+1, y),(x,y)):
        yield grid[y][x+1]
    if y > 0 and not grid[y-1][x].previous and legal_proceed((x, y-1),(x,y)):
        yield grid[y-1][x]
    if y < len(grid) - 1 and not grid[y+1][x].previous and legal_proceed((x, y+1),(x,y)):
        yield grid[y+1][x]


# Attempt to create Dijstra's algorithm
def do_dijkstra(start_loc: Node):
    p_queue = [(start_loc, 0, "START")] # implemented as a queue of lists of the form [node, loss, prev]
    while p_queue:
        current_cel = p_queue.pop(0)
        current_node = current_cel[0]
        current_node.total_loss = current_cel[1]
        current_node.previous = current_cel[2]
        q_vals = [v[0] for v in p_queue]
        for link in get_neighbour(current_node.x, current_node.y): # gotta check for legal to proceed
            if link in q_vals:
                temp = list(p_queue.pop(q_vals.index(link)))
                if temp[1] > current_node.total_loss + temp[0].value:
                    temp[1] = current_node.total_loss + temp[0].value
                    temp = tuple(temp)
            else:
                temp = (link, current_node.total_loss + link.value, current_node)
            p_queue.append(temp)
        p_queue.sort(key=lambda x: x[1])
        print(f"{current_node}: {p_queue}")

def find_path(end):
    print("path")
    global grid
    x, y = end
    hist = [end]
    prev = grid[y][x].previous
    while prev != "START":
        hist.append((prev.x, prev.y))
        x, y = prev.x, prev.y
        prev = grid[y][x].previous
        print(hist)
    return hist

if __name__ == '__main__':
    world = Cube(2)
    for i in range(1,7):
        world.sides[i].values=[[True, False],[False,True]]
    print(world.facing)
    for i in range(4):
        world.rotate("N")
        print(world.facing)
    for i in range(4):
        world.rotate("E")
        print(world.facing)
    # print(world)