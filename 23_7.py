TESTING = False
WILD = False
filename = "data/23_7_sample.txt" if TESTING else "data/23_7.txt"
TYPES = {"Five OAK": 7, "Four OAK": 6, "Full House": 5, "Three OAK": 4, "Two Pair": 3, "One Pair": 2, "High Card": 1}
CARDS = {"A":14, "K":13, "Q":12, "J":11, "T":10}
CARDS.update({str(i):i for i in range(2,10)})

class Hand:
    def find_hand_type(self):
        uniques = set(self.cards)
        if len(uniques) == 1:
            return "Five OAK"
        elif len(uniques) == 2:
            # Could be 4OAK or FH
            if self.cards.count(list(uniques)[0]) in [1,4]:
                return "Four OAK"
            else:
                return "Full House"
        elif len(uniques) == 3:
            #options are 3OAK or 2P
            counts = [self.cards.count(list(uniques)[i]) for i in range(len(uniques))]
            if 3 in counts:
                return "Three OAK"
            else:
                return "Two Pair"
        elif len(uniques) == 4:
            return "One Pair"
        else:
            return "High Card"

    def find_wild_hand_type(self):
        uniques = set([c for c in self.cards if c != "J"])
        jokers = self.cards.count("J")
        if jokers == 0:
            return self.find_hand_type()
        counts = [self.cards.count(list(uniques)[i]) for i in range(len(uniques))]
        counts.sort(reverse=True)
        # do this based on counts[0] to start with
        if not counts:
            return self.find_hand_type()
        elif counts[0] + jokers == 5:
            return "Five OAK"
        elif counts[0] + jokers == 4:
            return "Four OAK"
        elif counts[0] + jokers == 3 and len(counts) == 2:
            return "Full House"
        elif counts[0] + jokers == 3:
            return "Three OAK"
        elif counts[0] + jokers == 2:
            return "One Pair"
        return "High Card"

    def hand_score(self):
        # Do string shit to get a score
        score = [CARDS[card] for card in self.cards]
        out = 0
        value = 1000000000
        for i in range(len(score)):
            out += score[i] * value
            value //= 100
        return out

    def __init__(self, string):
        string = string.strip()
        string = string.split()
        self.bid = int(string[1])
        self.cards = list(string[0])
        self.type = self.find_hand_type() if not WILD else self.find_wild_hand_type()
        self.type_score = TYPES[self.type]

    def __str__(self):
        return f"{''.join(self.cards)}, {self.type}. Bid: {self.bid}" #. Hand score {self.hand_score()}"


if __name__ == "__main__":
    with open(filename, "r") as f:
        data = f.read()
    data = data.split("\n")
    hands = []
    for datum in data:
        hands.append(Hand(datum))
    hands = list(sorted(hands, key=lambda hand: (hand.type_score, hand.hand_score())))
    score = 0
    for i, hand in enumerate(hands,1):
        print(i, hand)
        score += hand.bid * i
    print(f"Part 1 score {score}")
    # Time for Jokers!
    WILD = True
    CARDS["J"] = 1
    hands = []
    for datum in data:
        # print()
        # print(datum)
        hands.append(Hand(datum))
        # print(hands[-1])
    hands = list(sorted(hands, key=lambda hand: (hand.type_score, hand.hand_score())))
    score = 0
    for i, hand in enumerate(hands,1):
        print(i, hand)
        score += hand.bid * i
    print(f"Part 2 score {score}")
    if score <= 252762566:
        print("It's too low")

# 252762566 too low