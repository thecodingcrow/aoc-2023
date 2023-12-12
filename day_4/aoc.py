import re
from pprint import pprint

with open("input.txt") as file:
    lines = [line for line in file.read().splitlines()]

    card_values = []
    duplicated_cards = {}

    at_line = 0

    for index, line in enumerate(lines):
        winning_numbers = re.findall(
            r"\d+", line.split("|")[0][line.split("|")[0].index(":") + 1 :]
        )
        my_numbers = re.findall(r"\d+", line.split("|")[1])

        wins = sum([number in winning_numbers for number in my_numbers])
        print("Wins for line", index + 1, wins)
        copies = 0

        if index + 1 in duplicated_cards:
            copies = duplicated_cards[index + 1]
            print("Found", copies, "copies of card", index + 1)

        for i in range(wins):
            print("In line", index + 1, ". Duplicate row number", index + i + 2)

            if not index + i + 2 in duplicated_cards:
                duplicated_cards[index + i + 2] = 1
            else:
                duplicated_cards[index + i + 2] += 1

        if copies:
            print("\n")
            print("Adding wins from copy")
            for i in range(wins):
                print(
                    "In line",
                    index + 1,
                    ". adding",
                    copies,
                    "copies of card",
                    index + i + 2,
                )

                if not index + i + 1 in duplicated_cards:
                    duplicated_cards[index + i + 2] = copies
                else:
                    duplicated_cards[index + i + 2] += copies

        print("\n")

        # card_value = round(
        #     2 ** (sum([number in winning_numbers for number in my_numbers]) - 1)
        # )

        # card_values.append(card_value)

    # print("Sum of all card values: ", sum(card_values))
    print("Copied cards", duplicated_cards)

    total_sum_of_cards = 0

    for index, _ in enumerate(lines):
        total_sum_of_cards += 1

        if index + 1 in duplicated_cards:
            total_sum_of_cards += duplicated_cards[index + 1]

    print("Total number of scratch cards", total_sum_of_cards)
