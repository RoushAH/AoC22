from functools import lru_cache

MAX_TIME = 26
global valves
global starter

#links takes a dict of valves keyed to the distance to that valve, ignoring cap 0 valves
class Valve:
    def __init__(self, name, capacity, links=None):
        self.name = name
        self.capacity = capacity
        self.links = links

    def __str__(self):
        return f"{self.name}: {self.capacity}; => {self.links}"

# get data in strings, convert to a dict of valve objects
def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.readlines()

    data = list(map(lambda x: x.replace("\n",""), data))
    rooms = {}
    valves = {}
    for val in data:
        name = val[6:8]
        capacity = int(val[val.find("=")+1:val.find(";")])
        links = val.split(",")
        links[0] = links[0][-2:]
        links = list(map(lambda x: x.strip(), links))
        rooms[name] = links
        if capacity > 0:
            valves[name] = Valve(name, capacity)
    return rooms, valves

# Attempt to create Dijstra's algorithm
def do_dijkstra(rooms: dict[str, list[str]], start_room: str, valves):
    t = 0
    p_queue = [[start_room, 0]] # implemented as a queue of lists of the form [room, dist]
    distances = {}
    while p_queue:
        current_node = p_queue.pop(0)
        current_room = current_node[0]
        distances[current_room] = current_node[1]
        t = current_node[1]
        for link in rooms[current_room]:
            if link not in distances:
                if link in p_queue:
                    temp = p_queue.pop(p_queue.index(link))
                    if temp[1] > t+1:
                        temp[1] = t+1
                else:
                    temp = [link, t+1]
                p_queue.append(temp)
        p_queue.sort(key=lambda x: x[1])
    return_dict = {}
    for key in valves:
        return_dict[key] = distances[key]
    if start_room in return_dict:
        return_dict.pop(start_room)
    return return_dict

def time_cost(items):
    if not items:
        return 0
    time = len(items)
    last = starter
    for i in range(len(items)):
        next_node = items[i]
        time += last.links[next_node]
        last = valves[next_node]
    return time

def permutate(vals: list[str], current =None ):
    # print(vals, current)
    if current is None:
        current = []
    if len(vals) == 0:
        yield tuple(current)
    elif time_cost(current) > MAX_TIME:
        # print(time_cost(current), current)
        yield tuple(current[:-1])
    else:
        for i in range(len(vals)):
            for output in permutate([x for x in vals if x != vals[i]], current + [vals[i]]):
                yield output
    # return output

def calculate_pressure(steps):
    time = 0
    final_pressure = 0
    last = starter
    for step in steps:
        time += 1 + last.links[step]
        if time >= MAX_TIME:
            return final_pressure
        final_pressure += (MAX_TIME-time) * valves[step].capacity
        last = valves[step]
    return final_pressure

# Given a list of options, find the best one
def find_best(list_of_options):
    max_pressure = 0
    best_option = None
    perms = permutate([name for name in list_of_options])
    for option in perms:
        pressure = calculate_pressure(list(option))
        if pressure > max_pressure:
            max_pressure = pressure
            best_option = option
    return max_pressure, best_option

# Given a list of options and a minimum standard, find all that exceed that minimum
def find_possible(list_of_options, minimum_standard):
    winners = []
    perms = permutate([name for name in list_of_options])
    for option in perms:
        pressure = calculate_pressure(list(option))
        if pressure > minimum_standard:
            winners.append((option, pressure))
    return winners

# game plan:
# 1: pull in data, create room dict and valve objects if needed
# 2: dijkstra for each valve, and store that as the links for the given valve
# 3: output the permutations of the valves
# 4: calculate the pressure release for each permutation
# 5: output the highest of these
if __name__ == '__main__':
    global valves
    global starter
    rooms, valves = parse_input('day16.txt')
    for name in valves:
        valves[name].links = do_dijkstra(rooms, name, valves)
        print(valves[name])
    starter = Valve("AA", 0, do_dijkstra(rooms, "AA", valves))
    print(starter)
    # Find my best 26-minute run
    max_pressure, best_option = find_best([name for name in valves])
    print(max_pressure, best_option)
    print([name for name in valves if name not in best_option])
    # Finding the best option for the elephant given the best option
    replacement, elephant_steps = find_best([name for name in valves if name not in best_option])
    print(f"Replacement value is {replacement}, for {elephant_steps}")
    # Finding the list of options that exceed the replacement value
    better_options = find_possible([name for name in valves], minimum_standard=replacement)
    print(len(better_options))
    # Find best combo for the better options
    best_pressure = max_pressure + replacement
    best_choices = best_option + elephant_steps
    i = 0
    for option in better_options:
        i += 1
        steps, pressure = option[0], option[1]
        p_pressure, p_steps = find_best([name for name in valves if name not in steps])
        if pressure + p_pressure > best_pressure:
            best_pressure = pressure + p_pressure
            best_choices = steps + p_steps
        if i % 100 == 0:
            print(f"{i} {best_pressure}: {best_choices}")
    print(best_choices)
    print(best_pressure)

#2208 too low
