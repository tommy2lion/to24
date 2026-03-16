# set_ops.py
from fractions import Fraction
from typing import Set, Union, List

Number = Union[int, Fraction]

def combine(set1: Set[Number], set2: Set[Number]) -> Set[Number]:
    """
    Return a set of all non-negative numbers obtained by applying +, -, *, /
    (both orders for subtraction and division) to elements from set1 and set2.
    """
    if not set1 or not set2:
        return set()
    results = set()
    for a in set1:
        for b in set2:
            results.add(a + b)
            results.add(abs(a - b))          # covers a-b and b-a
            results.add(a * b)
            if b != 0:
                results.add(Fraction(a, b))
            if a != 0:
                results.add(Fraction(b, a))
    return results

def combine_all(sets: List[Set[Number]]) -> Set[Number]:
    """
    Left-associative combine of multiple sets.
    """
    if not sets:
        return set()
    result = sets[0]
    for s in sets[1:]:
        result = combine(result, s)
    return result