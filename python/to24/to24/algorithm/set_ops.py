# set_ops.py
from fractions import Fraction
from typing import Set, Union, List

Number = Union[int, Fraction]

def combine(set1: Set[Number], set2: Set[Number]) -> Set[Number]:
    """
    Return a set of all non‑negative numbers that can be obtained by applying
    addition, subtraction (absolute difference), multiplication, and division
    (both orders) to one element from set1 and one from set2.

    Args:
        set1: A set of numbers (int or Fraction).
        set2: Another set of numbers.

    Returns:
        A set of non‑negative numbers (int or Fraction) resulting from the operations.
    """
    if not set1 or not set2:
        return set()

    results = set()
    for a in set1:
        for b in set2:
            # addition
            results.add(a + b)
            # subtraction (absolute value covers both a-b and b-a)
            results.add(abs(a - b))
            # multiplication
            results.add(a * b)
            # division a / b (b != 0)
            if b != 0:
                results.add(Fraction(a, b))
            # division b / a (a != 0)
            if a != 0:
                results.add(Fraction(b, a))
    return results


def combine_all(sets: List[Set[Number]]) -> Set[Number]:
    """
    Apply combine repeatedly to a list of sets in a left‑associative manner.
    For example, combine_all([set1, set2, set3]) returns combine(combine(set1, set2), set3).

    Args:
        sets: A list of sets of numbers.

    Returns:
        The final set after combining all sets.
    """
    if not sets:
        return set()
    result = sets[0]
    for s in sets[1:]:
        result = combine(result, s)
    return result