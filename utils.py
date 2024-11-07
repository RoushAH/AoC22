def ints_in_range(low, high):
    ''' Return the number of ints between low and high. Non-inclusive '''
    low = int(low+1)
    if int(high) == high:
        high = int(high)
    else:
        high = int(high + 1)
    return high - low

def get_file_name(stage, file):
    filename = file.split("\\")[-1].split(".")[0]
    if stage == 0:
        return f"data/{filename}.txt"
    else:
        return f"data/{filename}_sample{stage}.txt"

def get_data(stage, file, string = None):
    filename = get_file_name(stage, file)
    with open(f"{filename}", "r") as f:
        data = f.read()
    return data.split("\n") if not string else data
