# set_based.py
from fractions import Fraction
from typing import Tuple
from .set_ops import combine
from .combo_cache import NumberCombo

class SetBasedSolver:
    """
    24-game solver that enumerates all 1-3 and 2-2 partitions.
    Uses NumberCombo to obtain pre‑computed results for two and three numbers.
    """

    def __init__(self):
        self._combo = NumberCombo()   # internal cache

    def solve(self, a: int, b: int, c: int, d: int,
              target: int = 24, return_expr: bool = False):
        nums = [Fraction(x) for x in (a, b, c, d)]
        target_frac = Fraction(target)

        # 1‑3 partitions: pick one number as singleton, the other three together
        for i in range(4):
            single = nums[i]
            three = nums[:i] + nums[i+1:]
            three_res = self._combo.three_results(*three)
            if target_frac in combine({single}, three_res):
                if return_expr:
                    expr = self._build_expr(nums, target_frac)
                    return True, expr
                return True

        # 2‑2 partitions: three unordered pairings
        pairings = [
            ((0,1), (2,3)),   # (a,b) & (c,d)
            ((0,2), (1,3)),   # (a,c) & (b,d)
            ((0,3), (1,2))    # (a,d) & (b,c)
        ]
        for idx1, idx2 in pairings:
            pair1 = [nums[i] for i in idx1]
            pair2 = [nums[i] for i in idx2]
            res1 = self._combo.two_results(*pair1)
            res2 = self._combo.two_results(*pair2)
            if target_frac in combine(res1, res2):
                if return_expr:
                    expr = self._build_expr(nums, target_frac)
                    return True, expr
                return True

        return (False, "") if return_expr else False

    def _build_expr(self, nums, target_frac):
        """Fallback to simple algorithm to obtain an expression."""
        from .simple import Simple
        simple = Simple()
        a, b, c, d = (int(x) for x in nums)
        _, expr = simple.solve(a, b, c, d, return_expr=True)
        return expr