# set_based.py
from itertools import combinations
from fractions import Fraction
from typing import Set, Tuple
from .set_ops import combine

class SetBasedSolver:
    """
    A 24‑game solver based on set partitioning and caching.
    Numbers are treated as a multiset; a sorted tuple is used as the cache key.
    """

    def __init__(self):
        # Cache: sorted tuple of Fractions -> set of Fractions (all possible results)
        self._cache = {}

    def solve(self, a: int, b: int, c: int, d: int,
              target: int = 24, return_expr: bool = False):
        """
        Determine whether the four integers can yield the target value using +, -, *, /.

        Args:
            a, b, c, d: Four integers (each between 1 and 10)
            target: The target number, default 24
            return_expr: If True, also return a valid expression

        Returns:
            bool or (bool, str)
        """
        # Convert to Fraction for exact arithmetic, then sort to get a canonical multiset key
        nums = [Fraction(x) for x in (a, b, c, d)]
        nums_sorted = tuple(sorted(nums))
        target_frac = Fraction(target)

        # Compute all possible results for this multiset
        all_results = self._compute(nums_sorted)

        if target_frac in all_results:
            if return_expr:
                expr = self._build_expr(nums, target_frac)
                return True, expr
            return True
        return (False, "") if return_expr else False

    def _compute(self, num_tuple: Tuple[Fraction, ...]) -> Set[Fraction]:
        """
        Recursively compute all possible results for a sorted tuple of numbers (multiset).
        """
        if num_tuple in self._cache:
            return self._cache[num_tuple]

        # Single number: the result is the number itself
        if len(num_tuple) == 1:
            self._cache[num_tuple] = {num_tuple[0]}
            return {num_tuple[0]}

        n = len(num_tuple)
        results = set()
        indices = list(range(n))

        # Generate all proper non‑empty subsets of indices (size 1 .. n-1)
        for k in range(1, n):
            for comb in combinations(indices, k):
                # Build the two sub‑multisets (sorted)
                group1_vals = tuple(sorted(num_tuple[i] for i in comb))
                group2_vals = tuple(sorted(num_tuple[i] for i in indices if i not in comb))

                # Recursively compute results for both groups
                res1 = self._compute(group1_vals)
                res2 = self._compute(group2_vals)

                # Combine the two result sets
                results.update(combine(res1, res2))

        self._cache[num_tuple] = results
        return results

    def _build_expr(self, nums, target_frac):
        """
        Build an expression that yields the target value.
        Since a solution is known to exist, fall back to the simple algorithm
        (it is straightforward and reliable).
        """
        # Import dynamically to avoid circular dependency
        from .simple import Simple
        simple = Simple()
        a, b, c, d = (int(x) for x in nums)
        _, expr = simple.solve(a, b, c, d, return_expr=True)
        return expr