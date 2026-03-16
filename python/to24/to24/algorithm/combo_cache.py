# combo_cache.py
from fractions import Fraction
from typing import Set, Tuple, Dict
from .set_ops import combine

class NumberCombo:
    """
    Caches results for two and three numbers to avoid redundant computation.
    Useful when the same number combinations appear multiple times (e.g., in set_based solver).
    """

    def __init__(self):
        self._two_cache: Dict[Tuple[Fraction, ...], Set[Fraction]] = {}
        self._three_cache: Dict[Tuple[Fraction, ...], Set[Fraction]] = {}

    def two_results(self, a: Fraction, b: Fraction) -> Set[Fraction]:
        """
        Return all non‑negative results from combining a and b.
        The pair (a,b) is considered unordered; the result is cached.
        """
        key = tuple(sorted([a, b]))
        if key not in self._two_cache:
            self._two_cache[key] = combine({a}, {b})
        return self._two_cache[key]

    def three_results(self, a: Fraction, b: Fraction, c: Fraction) -> Set[Fraction]:
        """
        Return all non‑negative results from combining a, b, c.
        The triple is considered unordered; the result is cached.
        """
        key = tuple(sorted([a, b, c]))
        if key in self._three_cache:
            return self._three_cache[key]

        x, y, z = key   # now x ≤ y ≤ z
        # Three possible binary tree structures for three numbers:
        # (x op y) op z
        s1 = combine(self.two_results(x, y), {z})
        # (x op z) op y
        s2 = combine(self.two_results(x, z), {y})
        # (y op z) op x
        s3 = combine(self.two_results(y, z), {x})

        result = s1 | s2 | s3
        self._three_cache[key] = result
        return result