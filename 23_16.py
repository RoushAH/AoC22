from utils import get_data

if __name__ == "__main__":
    stage = 0
    data = get_data(stage=stage, file=__file__)
    records = [list(l) for l in data]
    print(records)