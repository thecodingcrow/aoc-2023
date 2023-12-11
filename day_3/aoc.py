import re
from pprint import pprint


def get_parts_from_line(matrix, line_number, start_index, parts):
    reduced_line = matrix[line_number][start_index:]

    a_is_part, b_is_part, c_is_part = False, False, False
    a_slice = re.search(r".\d+.", reduced_line)

    if a_slice == None:
        return parts

    a_coords = list(a_slice.span())
    a_is_part = sum(
        [
            c != "." and (not c.isdigit())
            for c in [a_slice.group()[0], a_slice.group()[-1]]
        ]
    )

    if line_number >= 1:
        b_slice = matrix[line_number - 1][start_index:][
            int(a_coords[0]) : int(a_coords[1])
        ]
        b_is_part = sum([c != "." for c in b_slice])

    if line_number + 1 < len(matrix):
        c_slice = matrix[line_number + 1][start_index:][
            int(a_coords[0]) : int(a_coords[1])
        ]
        c_is_part = sum([c != "." for c in c_slice])

    if a_is_part or b_is_part or c_is_part:
        part_obj = {
            "part": int(re.search(r"\d+", a_slice.group()).group()),
            "span": a_coords,
        }
        parts.append(part_obj)

    start_index = start_index + a_slice.end() - 1

    return get_parts_from_line(matrix, line_number, start_index, parts)


def calculate_sum_of_valid_parts():
    sum_of_valid_parts = 0
    for index, _ in enumerate(lines):
        parts = get_parts_from_line(lines, index, 0, [])
        sum_of_valid_parts += sum([int(part) for part in parts])

    print("Sum of all valid parts:", sum_of_valid_parts)


def is_span_overlapping(gear_span, part_span):
    return (gear_span[0] <= part_span[0] < gear_span[1]) or (
        gear_span[0] < part_span[1] <= gear_span[1]
    )


def get_parts_from_line_2(line, parts, index_shift):
    match = re.search(r"\d+", line)

    if match == None:
        return parts

    if match:
        part = {
            "part": match.group(),
            "span": (match.span()[0] + index_shift, match.span()[1] + index_shift),
        }

        parts.append(part)

    start_index = match.end()
    new_line = line[start_index:]

    return get_parts_from_line_2(new_line, parts, start_index + index_shift)


def get_gears_from_line(matrix, line_number, start_index, gears):
    parts_center, parts_lower, parts_upper = None, None, None
    reduced_line = matrix[line_number][start_index:]

    gear_slice = re.search(r".\*.", reduced_line)

    if gear_slice == None:
        return gears

    gear_coords = [
        gear_slice.span()[0] + start_index,
        gear_slice.span()[1] + start_index,
    ]

    hits = []

    parts_center = get_parts_from_line_2(matrix[line_number], [], 0)

    if line_number >= 1:
        parts_upper = get_parts_from_line_2(matrix[line_number - 1], [], 0)

    if line_number + 1 < len(matrix):
        parts_lower = get_parts_from_line_2(matrix[line_number + 1], [], 0)

    if parts_center:
        for part in parts_center:
            if is_span_overlapping(gear_coords, part["span"]):
                hits.append(part)

    if parts_upper:
        for part in parts_upper:
            if is_span_overlapping(gear_coords, part["span"]):
                hits.append(part)

    if parts_lower:
        for part in parts_lower:
            if is_span_overlapping(gear_coords, part["span"]):
                hits.append(part)

    if len(hits) == 2:
        gears.append(hits)
        print(
            "For gear",
            gear_slice.group(),
            "in line",
            line_number + 1,
            "at",
            gear_coords,
            ", we found",
            len(hits),
            "hits",
        )
        print(hits)
        print("\n\n")

    start_index = start_index + gear_slice.end() - 1

    return get_gears_from_line(matrix, line_number, start_index, gears)


with open("input.txt") as file:
    lines = [line for line in file.read().splitlines()]

    gears = []

    for index, _ in enumerate(lines):
        line_gears = get_gears_from_line(lines, index, 0, [])

        if line_gears:
            gears.append(line_gears)

    gear_sum = 0
    for line in gears:
        for ratio in line:
            gear_sum += int(ratio[0]["part"]) * int(ratio[1]["part"])

    print("Sum of all valid gear ratios", gear_sum)
