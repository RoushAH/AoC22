U = ( 0,  1)
D = ( 0, -1)
L = (-1,  0)
R = ( 1,  0)
directions = {"U":U, "D":D, "L":L, "R":R}

def merge(list_a, list_b):
    if len(list_a) != len(list_b):
        raise ValueError("Lists must have the same length")
    else:
        return [
            list_a[i] + list_b[i] for i in range(len(list_a))
        ]

def avg_int(a, b):
    """ Returns the integer average of a and b"""
    return (a + b) // 2

class rope:
    def __init__(self):
        self.head = [0,0]
        self.tail = [0,0]
        self.history = []

    def touching(self):
        # fail if the tail is over 1 space away from the head in any direction
        if abs(self.head[0] - self.tail[0]) > 1:
            return False
        if abs(self.head[1] - self.tail[1]) > 1:
            return False
        return True

    def move_step(self, direction):
        self.head = merge(self.head, directions[direction])
        if not self.touching():
            # we should be exactly 2 spaces apart
            if self.head[0] == self.tail[0] or self.head[1] == self.tail[1]:
                # we are in the same row or column
                self.tail[0] = avg_int(self.head[0], self.tail[0])
                self.tail[1] = avg_int(self.head[1], self.tail[1])
            else:
                # We are on a diagonal
                self.tail[0] += 1 if self.head[0] > self.tail[0] else -1
                self.tail[1] += 1 if self.head[1] > self.tail[1] else -1

    def move(self,direction, distance):
        for step in range(distance):
            self.move_step(direction)
            self.history.append(tuple(self.tail))


def touching(head, tail):
    # fail if the tail is over 1 space away from the head in any direction
    if abs(head[0] - tail[0]) > 1:
        return False
    if abs(head[1] - tail[1]) > 1:
        return False
    return True


class rope_n:
    def __init__(self, knots):
        self.knots = [[0,0] for _ in range(knots+1)]
        self.history = []

    def move_step(self, direction):
        self.knots[0] = merge(self.knots[0], directions[direction])
        for i in range(len(self.knots) - 1):
            head = self.knots[i]
            tail = self.knots[i+1]
            if not touching(head, tail):
                # we should be exactly 2 spaces apart
                if head[0] == tail[0] or head[1] == tail[1]:
                    # we are in the same row or column
                    tail[0] = avg_int(head[0], tail[0])
                    tail[1] = avg_int(head[1], tail[1])
                else:
                    # We are on a diagonal
                    tail[0] += 1 if head[0] > tail[0] else -1
                    tail[1] += 1 if head[1] > tail[1] else -1

    def move(self,direction, distance):
        for step in range(distance):
            self.move_step(direction)
            self.history.append(tuple(self.knots[-1]))


if __name__ == "__main__":
    test = input("Run test case? Y/N")
    if test.upper() == "Y":
        file = "day9sample.txt"
    else:
        file = "day9.txt"
    with open(file) as f:
        data = f.readlines()
    # data is noisy, strip out trailing \ns and then break into direction/distance pairs
    data = list(map(lambda x: x.replace("\n",""), data))
    data = list(map(lambda x: x.split(" "), data))
    # Now convert distance into an int and the pair to a tuple for... reasons...
    for val in data:
        val[1] = int(val[1])
    data = list(map(lambda x: tuple(x), data))
    # create the rope and run the steps
    rope = rope_n(9)
    for step in data:
        rope.move(*step)
    goal = rope.history
    goal = set(goal)
    # print(goal)
    print(len(goal))