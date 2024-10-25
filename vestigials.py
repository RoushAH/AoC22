
class Face:
    def __init__(self, size):
        self.size = size
        self.values = [[False for i in range(size)] for j in range(size)]
        # sides in order east, south, west, north
        self.neighbours = deque([0,0,0,0])

    def rotate(self, direction):
        if direction < 0:
            direction = -1
        elif direction > 0:
            direction = 1
        self.values = rotate(self.values, direction)
        self.neighbours.rotate(direction)

    def __str__(self):
        output = ""
        for i in range(len(self.values)):
            for j in range(len(self.values[i])):
                if self.values[i][j]:
                    output += OPEN
                else:
                    output += WALL
            output += "\n"
        return output

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

if __name__ == '__main__':
    world = Cube(2)
    for i in range(1,7):
        world.sides[i].values=[[True, False],[False,True]]
    print(world.facing)
    for i in range(4):
        world.rotate("N")
        print(world.facing)