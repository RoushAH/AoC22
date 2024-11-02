TESTING = False
filename = "data/23_4_sample.txt" if TESTING else "data/23_4.txt"
MARKERS = ['seed-to-soil map:', 'soil-to-fertilizer map:', 'fertilizer-to-water map:', 'water-to-light map:',
           'light-to-temperature map:', 'temperature-to-humidity map:', 'humidity-to-location map:', 'END_MARKER']
converters = []

def do_conversion(num_in, converter_list):
    # Take in the number in and the specific converter, and do the conversion
    for converter in converter_list:
        if converter[1] <= num_in < (converter[1] + converter[2]):
            return (converter[0] - converter[1]) + num_in
    return num_in

if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    seeds = data[0].split(":")[1].split()
    seeds = [int(i) for i in seeds]
    data = data[1:]
    data.append(None)
    data.append("END_MARKER")
    print(data)
    for i in range (len(MARKERS)-1):
        converter = data[data.index(MARKERS[i])+1:data.index(MARKERS[i+1])-1]
        converter = [i.split() for i in converter]
        converter = [[int(i) for i in j] for j in converter]
        converter = sorted(converter, key=lambda x: x[0])
        # converter.append([converter[-1][0] + converter[-1][2]]) # Pad with a finishing move
        print(converter)
        converters.append(converter)
    seed_locs = {}
    for seed in seeds:
        loc = seed
        for converter in converters:
            # print(converter, seed)
            seed = do_conversion(seed, converter)
        print(f"{loc} with {seed}")
        seed_locs[loc] = seed
    print(f"Part 1 answer is {min(seed_locs.values())}")
