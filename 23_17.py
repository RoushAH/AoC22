# Iterate down the major diagonal to find the minimum bid
# Dijkstra-man!
# Do Dijkstra for each cel, treating each as a little node
# Perhaps replace the 2d grid with a grid of node objects?
# Each having edge detection ability, a heat value, and a "previous".
# On discovery, store a node, then check to see which nodes you can legally reach.
# Implement a "can proceed" boolean function

from utils import get_data
grid = []

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.left = None
        self.right = None
        self.above = None
        self.below = None
        self.previous = None


if __name__ == "__main__":
    stage = 0
    data = get_data(stage, __file__, string=True)
    grid = data.split("\n")