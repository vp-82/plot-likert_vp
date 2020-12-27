"""
Module for computing the best interval for the x-ticks on a plot
"""

import typing


import numpy as np


def get_next_interval_divisor() -> typing.Generator[int, None, None]:
    """
    A generator that yields 5, and then successive powers of 10
    """
    yield 5
    yield 10
    yield 25
    yield 50
    i = 1
    while True:
        i += 1
        yield 10 ** i


def get_biggest_divisor(n: int) -> int:
    """
    Returns the largest divisor, from those generated by get_next_interval_divisor(),
    that divides the given number without a remainder.
    """
    biggest_divisor = 1
    for divisor in get_next_interval_divisor():
        if divisor > n:
            return biggest_divisor

        if n % divisor == 0:
            biggest_divisor = divisor

    raise RuntimeError(
        "this should never be reached because get_next_interval_divisor returns increasingly big numbers"
    )  # needed for type-checking


def get_best_interval_in_list(candidate_intervals: typing.List[int]) -> int:
    """
    Given a list of values, returns the one with the largest divisor (as defined above)
    """
    candidate_divisors = list(map(get_biggest_divisor, candidate_intervals))
    best_candidate = np.argmax(candidate_divisors)
    best_interval = candidate_intervals[best_candidate]

    return best_interval


def get_interval_for_scale(tick_space: int, max_width: int) -> int:
    """
    Given a width of the plot (max_width) and a suggested number of tick marks (tick_space),
    return the "best" interval to use between tick marks.
    """
    min_ticks = tick_space - 5
    max_ticks = tick_space + 2
    min_interval = max(
        1, int(max_width / max_ticks)
    )  # to ensure zero can't be an interval
    max_interval = round(max_width / min_ticks)

    candidate_intervals = list(range(min_interval, max_interval + 1))
    return get_best_interval_in_list(candidate_intervals)
