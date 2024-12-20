# Compare two lists. Return True if a[i] >= b[i] for all i
def compare(list_a, list_b, comparator=None):
    if len(list_a) != len(list_b):
        raise ValueError("Lists must have the same length")
    elif comparator is None:
        raise ValueError("Comparator must be specified")
    elif comparator not in ['>', '<', '>=', '<=', '==', '!=']:
        raise ValueError("Comparator must be one of '>', '<', '>=', '<=', '==', '!='")
    else:
        for i in range(len(list_a)):
            if not eval(str(list_a[i]) + comparator + str(list_b[i])):
                return False
        return True


# Add/subtract two lists
def merge(list_a, list_b, direction=None):
    if len(list_a) != len(list_b):
        raise ValueError("Lists must have the same length")
    if direction is None:
        raise ValueError("direction must be specified")
    elif direction not in ['+', '-', '*', '/', '%']:
        raise ValueError("direction must be one of '+', '-', '*', '/', '%'")
    return [
        eval(str(list_a[i]) + direction + str(list_b[i])) for i in range(len(list_a))
    ]


def rectangularise(items, filler):
    """ Pass a list of strings and a filler char. Fills each row, at the end, so they're all same length"""
    lens = [len(x) for x in items]
    max_len = max(lens)
    for row in range(len(items)):
        if lens[row] < max_len:
            items[row] = items[row] + filler * (max_len - lens[row])
    lens = [len(x) for x in items]


def rotate(values, direction=None):  # rotates a square array
    """ Rotates a square array. Direction is >0 for clockwise, <0 for counter-clockwise"""
    if len(values) != len(values[0]):
        raise ValueError("Array must be square")
    if direction is None:
        raise ValueError("direction must be specified")
    new_vals = []
    size = len(values)
    if direction > 0:
        for i in range(size):
            new_vals.append([
                values[j][i]
                for j in range(size - 1, -1, -1)])
    elif direction < 0:
        for j in range(size - 1, -1, -1):
            new_vals.append([
                values[i][j]
                for i in range(size)])
    return new_vals

def flip_2d(grid):
    out = [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]
    return out


def show_2d(values):
    output = ["".join(values[i]) for i in range(len(values))]
    output = "\n".join(output)
    print(output)

def pad_2d(group_of_items, filler):
    for row in group_of_items:
        row.insert(0, filler)
        row.append(filler)
    filler_2d = [[filler for i in range(len(group_of_items[0]))]]
    group_of_items = filler_2d + group_of_items + filler_2d
    return group_of_items

def starts_with(big, little):
    big = tuple(big[:len(little)])
    little = tuple(little)
    return big == little

def ends_with(big, little):
    big = tuple(big[-len(little):])
    little = tuple(little)
    return big == little

def harvest_string(value, direction, grid):
    """ Returns the valid component of the string, ignoring blanks, and the count of blanks removed from the beginning"""
    if direction.lower() in ["h", "e", "w"]:
        return grid[value]
    str_out = ""
    for i in range(len(grid)):
        str_out += str(grid[i][value])
    return str_out

if __name__ == "__main__":
    print(x:=pad_2d([[1, 2, 3, 4, 5], [5, 1, 2, 3, 4]],0))
    print(flip_2d(x))