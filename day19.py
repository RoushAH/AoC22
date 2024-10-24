from listfuncs import compare, merge
from multiprocessing import Pool

MAX_TIME = 32
ORE_BOT = [1, 0, 0, 0]
CLAY_BOT = [0, 1, 0, 0]
OBSIDIAN_BOT = [0, 0, 1, 0]
GEODE_BOT = [0, 0, 0, 1]


class Blueprint:
    def __init__(self, string_recipe):
        self.id = int(string_recipe.split(":")[0][-2:].strip())
        tail = string_recipe.split(":")[1]
        tail = tail.split(".")
        self.ore_bot = [int(tail[0].split()[-2]), 0, 0, 0]
        self.clay_bot = [int(tail[1].split()[-2]), 0, 0, 0]
        self.obsidian_bot = [int(tail[2].split()[-5]), int(tail[2].split()[-2]), 0, 0]
        self.geode_bot = [int(tail[3].split()[-5]), 0, int(tail[3].split()[-2]), 0]

    def __str__(self):
        return f"BP{self.id}: \n Ore: {self.ore_bot}\n Clay:{self.clay_bot}\n Obsidian {self.obsidian_bot}\n Geode: {self.geode_bot}"


class System:
    def __init__(self, bots=None, resources=None):
        # ore, clay, obsidian, geode
        self.bots = [1, 0, 0, 0] if not bots else bots
        self.resources = [0, 0, 0, 0] if not resources else resources

    def __str__(self):
        return f"Bots: {self.bots}\nResources: {self.resources}"

def smart_insert(value: System, items: list[System]):
    # attempts to insert a new system. Set a flag (insert)
    # If the new system is better than a matching one, the matching one is nuked.
    # If a same or worse one is found, insert is dropped
    # if insert still up, do the insertion
    insert = True
    for item in items:
        if item.bots == value.bots and compare(item.resources, value.resources,">="):
            insert = False
        elif item.bots == value.bots:
            # We have an improved option
            items.remove(item)
    if insert:
        items.append(value)
    return items

def prune(system_list: list[System]):
    max_geode = 0
    max_gbots = 0
    max_obsidian = 0
    max_obots = 0
    max_clay = 0
    for system in system_list:
        if system.resources[3] > max_geode:
            max_geode = system.resources[3]
        if system.bots[3] > max_gbots:
            max_gbots = system.bots[3]
        if system.resources[2] > max_obsidian:
            max_obsidian = system.resources[2]
        if system.bots[2] > max_obots:
            max_obots = system.bots[2]
        if system.resources[1] > max_clay:
            max_clay = system.resources[1]
    # print(f"Geodes:{max_geode}, Gbots:{max_gbots}, Obsidian:{max_obsidian}, Obots:{max_obots}")
    if max_geode > 0:
        system_list = [
            state for state in system_list if state.resources[3] == max_geode
        ]
    elif max_gbots > 0:
        system_list = [
            state for state in system_list if state.bots[3] >= max_gbots-1
        ]
    elif max_obsidian > 0:
        system_list = [
            state for state in system_list if state.resources[2] >= max_obsidian-2
        ]

    # Should also prune for:
    # # Same bots, fewer resources. This needs culling
    # # Same overall needs culling
    # if len(system_list) < 5:
    #     for system in system_list:
    #         print(f"System: {system}")
    return system_list

def optimise(blueprint: Blueprint):
    # create a list of states, iterate over them, creating new states with the rule: if can build Obsidian, do it. Else, create all possible state options
    # I wonder if, should there be a state in which there is a geode bot, all other states should be dropped??
    states = [System()]
    for minute in range(1, MAX_TIME + 1):
        new_states = []
        for state in states:
            if compare(state.resources, blueprint.geode_bot, comparator='>='):
                # build a geode_bot if poss
                state.resources = merge(state.resources, blueprint.geode_bot, "-")
                state.resources = merge(state.resources, state.bots, "+")
                state.bots[3] += 1
                new_states.append(state)
                # print(minute, state)
            else:
                # try other 3 options: nothing, ore, clay, obsidian
                new_states.append(System(state.bots, merge(state.resources, state.bots, "+")))  # do nothing
                # build ore
                if compare(state.resources, blueprint.ore_bot, comparator='>='):
                    ore_state = System(state.bots, state.resources)
                    ore_state.resources = merge(state.resources, state.bots, "+")
                    ore_state.bots = merge(state.bots, ORE_BOT, "+")
                    ore_state.resources = merge(ore_state.resources, blueprint.ore_bot, "-")
                    new_states.append(ore_state)
                # build clay
                if compare(state.resources, blueprint.clay_bot, comparator='>='):
                    clay_state = System(state.bots, state.resources)
                    clay_state.resources = merge(state.resources, state.bots, "+")
                    clay_state.bots = merge(state.bots, CLAY_BOT, "+")
                    clay_state.resources = merge(clay_state.resources, blueprint.clay_bot, "-")
                    new_states.append(clay_state)
                # make the obsidian bot
                if compare(state.resources, blueprint.obsidian_bot, comparator='>='):
                    obsidian_state = System(state.bots, state.resources)
                    obsidian_state.resources = merge(state.resources, state.bots, "+")
                    obsidian_state.bots = merge(state.bots, OBSIDIAN_BOT, "+")
                    obsidian_state.resources = merge(obsidian_state.resources, blueprint.obsidian_bot, "-")
                    new_states.append(obsidian_state)
        states = prune(new_states)
        print(blueprint.id, minute, len(states))
        # if len(states) < 10:
        #     for s in states:
        #         print(s)
    return states

def handle(b:Blueprint):
    states = optimise(b)
    geodes = states[0].resources[3]
    print(f"BP{b.id}: Geodes {geodes}")
    return geodes


if __name__ == '__main__':
    filename = "day19.txt"
    with open(filename, 'r') as f:
        data = f.readlines()
    blueprints = [Blueprint(datum) for datum in data]
    if len(blueprints) > 3:
        blueprints = blueprints[:3]
    results = []
    # for b in blueprints:
    #     # print(b)
    #     states = optimise(b)
    #     geodes = states[0].resources[3]
    #     print(f"BP{b.id}: Geodes {geodes}")
    #     results.append(geodes)
        # quality_level += b.id*geodes
        # input()
    with Pool(processes=4) as pool:
        results = pool.map(handle, blueprints)
    print(results)
    quality_level = sum(results)
    print(f"Total quality level {quality_level}")