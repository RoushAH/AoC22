import itertools
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
        yield tuple(current)
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
    max_pressure = 0
    me_perms = permutate([name for name in valves])
    for option in me_perms:
        me_pressure = calculate_pressure(list(option))
        # print(option, me_pressure, [name for name in valves if name not in option])
        ellie_perms = permutate([name for name in valves if name not in option])
        for ellie_option in ellie_perms:
            ellie_pressure = calculate_pressure(list(ellie_option))

            if me_pressure + ellie_pressure > max_pressure:
                max_pressure = me_pressure + ellie_pressure
                print(max_pressure, option, ellie_option)
    print(max_pressure)

#2208 too low
