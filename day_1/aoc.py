import re


def find_first_occurrence(patterns, text):
    first_match = None
    first_index = len(text)

    for pattern in patterns:
        match = re.search(pattern, text)
        if match and match.start() < first_index:
            first_match = match
            first_index = match.start()

    return first_match


def find_first_number(line, direction="ltr"):
    numbers_as_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    if direction == "rtl":
        numbers_as_words = {
            key[::-1]: index + 1
            for index, (key, _) in enumerate(numbers_as_words.items())
        }
        line = line[::-1]

    firstWordMatch = find_first_occurrence(numbers_as_words, line)
    firstDigitMatch = re.search(r"\d", line)

    if not firstWordMatch:
        return firstDigitMatch.group()

    print(
        "Direction: ",
        direction,
        "Input: ",
        line if direction == "ltr" else line[::-1],
        "\n",
    )
    if firstWordMatch:
        print(
            "first word match",
            firstWordMatch.group()
            if direction == "ltr"
            else firstWordMatch.group()[::-1],
        )
    else:
        print("first word match", "not found")
    print("first digit match", firstDigitMatch.group())

    first_number = (
        str(numbers_as_words[firstWordMatch.group()]) if firstWordMatch else None
    )

    if firstDigitMatch.start() < firstWordMatch.start():
        first_number = firstDigitMatch.group()

    print("First number: ", first_number)
    print("*" * 20, "\n")

    return first_number


with open("input.txt") as file:
    lines = [line for line in file.read().splitlines()]

    sum_of_calibration_values = sum(
        [
            int(
                "".join(
                    [find_first_number(line), find_first_number(line, direction="rtl")]
                )
            )
            for line in lines
        ]
    )

    print(sum_of_calibration_values)
