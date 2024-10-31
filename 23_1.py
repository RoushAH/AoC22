TESTING = False
filename = "data/23_1_sample.txt" if TESTING else "data/23_1.txt"
DIGITS = {str(i):i for i in range(10)}
WORD_DIGITS = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
WORD_DIGITS.update(DIGITS)

def get_vals(string):
    first, last = None, None
    for char in string:
        if char in DIGITS:
            last = char
            if first is None:
                first = char
    return int(f"{first}{last}")

def get_vals_words(string):
    first, last = None, None
    for i in range(len(string)):
        for option in WORD_DIGITS:
            if string[i:].startswith(option):
                last = WORD_DIGITS[option]
                if first is None:
                    first = WORD_DIGITS[option]
    return int(f"{first}{last}")


if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    print(data)
    print(sum([get_vals_words(line) for line in data]))