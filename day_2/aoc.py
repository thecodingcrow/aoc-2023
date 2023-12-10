import re
from pprint import pprint


def is_draw_possible(configuration, draw):
    limit_red, limit_green, limit_blue = (
        configuration["red"],
        configuration["green"],
        configuration["blue"],
    )

    print(draw)

    if (
        ("red" in draw and int(draw["red"]) > limit_red)
        or ("blue" in draw and int(draw["blue"]) > limit_blue)
        or ("green" in draw and int(draw["green"]) > limit_green)
    ):
        return False

    return True


def find_sum_of_valid_games_for_config(
    configuration={"red": 12, "green": 13, "blue": 14}
):
    sum_of_valid_game_indizes = 0

    for index, game in enumerate(games):
        print("Game: ", index + 1, "\n")
        pprint(configuration)
        print("\n")
        game_counts = True

        for draw in game:
            if not is_draw_possible(configuration=configuration, draw=draw):
                game_counts = False
                print("Game is invalid")

        if game_counts:
            print("Game counts")
            sum_of_valid_game_indizes += index + 1
        print("\n")

    print("Valid games indizes summed up: ", sum_of_valid_game_indizes)


def find_power_of_minimum_neede_set(game):
    minimums = {"red": 0, "blue": 0, "green": 0}

    for draw in game:
        if "red" in draw and int(draw["red"]) > minimums["red"]:
            minimums["red"] = int(draw["red"])

        if "green" in draw and int(draw["green"]) > minimums["green"]:
            minimums["green"] = int(draw["green"])

        if "blue" in draw and int(draw["blue"]) > minimums["blue"]:
            minimums["blue"] = int(draw["blue"])

    return minimums["red"] * minimums["blue"] * minimums["green"]


with open("input.txt") as file:
    lines = [line for line in file.read().splitlines()]

    games = []

    for line in lines:
        first_game_start_index = re.search(r"Game [0-9]*: ", line).end()
        line = line[first_game_start_index::]

        raw_results = line.split(";")

        final = []

        for result in raw_results:
            results_dict = {}

            res = result.strip().split(",")
            for r in res:
                x = r.strip().split(" ")
                results_dict[x[1]] = x[0]

            final.append(results_dict)

        games.append(final)

    # pprint(games)

    # find_sum_of_valid_games_for_config()

    sum_of_powers = 0

    for index, game in enumerate(games):
        power = find_power_of_minimum_neede_set(game)
        print("Power of Game: ", power)

        sum_of_powers += power

    print("Total power of games: ", sum_of_powers)
