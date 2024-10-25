from collections import deque

TEST = False
KEY = 811589153
PART = 1

def derotate(items:list[int], starter=None):
    if starter is None:
        starter = 0
    items = deque(items)
    dist = items.index(starter)
    items.rotate(-dist)
    x = list(items)
    items.rotate(dist)
    return x

def find(val, list):
    for i in range(len(list)):
        if list[i] == val:
            return i
    return -1

def mix(items, original):
    if TEST:
        print(original, items)
    items = deque(items)
    for num in original:
        old_space = items.index(num)
        items.rotate(-old_space)
        items.popleft()
        items.rotate(-(num%(len(original)-1)))
        items.append(num)
        # print(num, derotate(items))
    final_rotation = items.index(0)
    items.rotate(-final_rotation)
    return list(items)

def mix_less_clever(items, order):
    for num in order:
        old_space = find(num, items)
        x = items.pop(old_space)
        old_space += num
        old_space %= len(items)
        items.insert(old_space, x)
        if TEST:
            print(num, items)
    return items


def mmix(enumerated: deque):
    """ Perform the mix algorithm on our enumerated deque of numbers """
    # Move each number once, using original indexes
    # We can't iterate over actual values from enumerated, since we'll be modifying it as we go
    for original_index in range(len(enumerated)):
        while enumerated[0][0] != original_index:  # bring our required element to the left end
            enumerated.rotate(-1)

        current_pair = enumerated.popleft()
        shift = current_pair[1] % len(enumerated)  # retrieve the value to move by; allow for wrapping over
        enumerated.rotate(-shift)  # rotate everything by n positions
        enumerated.append(current_pair)  # and now reinsert our pair at the end

        # print(enumerated)

    return enumerated

def value_at_n(values: list, n: int):
    """ Determine the value at position n in our list.
    If index is beyond the end, then wrap the values as many times as required. """
    digit_posn = (values.index(0)+n) % len(values)
    return values[digit_posn]

if __name__ == '__main__':
    filename = "data/day20sample.txt" if TEST else "data/day20.txt"
    with open(filename) as f:
        data = f.read().splitlines()
    # turn data into ints
    data = list(map(lambda x: int(x), data))
    original = tuple(data)
    # attempt = mix_less_clever(data, original)
    # print(derotate(attempt))
    # fixed = derotate(attempt)
    fixed = mix(data, original)
    positions = [1000,2000,3000]
    positions = list(map(lambda x: x % len(fixed), positions))
    print(positions, len(fixed))
    ans = 0
    for pos in positions:
        print(pos, fixed[pos])
        ans += fixed[pos]
    print(ans)

    enumerated = deque(list(enumerate(data.copy())))  # deque of tuples of (original index, value)
    enumerated = mmix(enumerated)

    print(fixed)
    print(enumerated)

    coord_sum = 0
    for n in (1000, 2000, 3000):
        # Turn our enumerated list into a list
        coord_sum += value_at_n([val[1] for val in enumerated], n)
    print(f"Part 1: {coord_sum}")

    new_data = [val*KEY for val in data]
    enumerated = deque(list(enumerate(new_data)))
    for i in range(10):
        enumerated = mmix(enumerated)
    coord_sum = 0
    for n in (1000, 2000, 3000):
        # Turn our enumerated list into a list
        coord_sum += value_at_n([val[1] for val in enumerated], n)
    print(f"Part 2: {coord_sum}")

