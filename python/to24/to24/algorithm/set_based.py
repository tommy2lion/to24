# set_based.py
from fractions import Fraction
from .set_ops import combine
from .combo_cache import NumberCombo

class SetBased:
    """
    24-game solver that enumerates all 1-3 and 2-2 partitions.
    Uses NumberCombo to obtain pre-computed results and expressions.
    """

    def __init__(self):
        self._combo = NumberCombo()

    def solve(self, a: int, b: int, c: int, d: int, return_expr: bool = False):
        # print(f"DEBUG: return_expr={return_expr}")
        nums = [Fraction(x) for x in (a, b, c, d)]
        target_frac = Fraction(24)

        # 1-3 partitions: pick one number as singleton, the other three together
        for i in range(4):
            single = nums[i]
            three = nums[:i] + nums[i+1:]
            three_map = self._combo.three_results_map(*three)
            # Combine singleton with three_map
            single_map = {single: str(single)}
            combined = self._combine_maps(single_map, three_map)
            if target_frac in combined:
                # print("DEBUG: found in 1-3 partition")
                if return_expr:
                    return True, combined[target_frac]
                return True

        # 2-2 partitions: three unordered pairings
        pairings = [
            ((0,1), (2,3)),   # (a,b) & (c,d)
            ((0,2), (1,3)),   # (a,c) & (b,d)
            ((0,3), (1,2))    # (a,d) & (b,c)
        ]
        for idx1, idx2 in pairings:
            pair1 = [nums[i] for i in idx1]
            pair2 = [nums[i] for i in idx2]
            map1 = self._combo.two_results_map(*pair1)
            map2 = self._combo.two_results_map(*pair2)
            combined = self._combine_maps(map1, map2)
            if target_frac in combined:
                # print("DEBUG: found in 2-2 partition")
                if return_expr:
                    return True, combined[target_frac]
                return True

        return (False, "") if return_expr else False

    def _combine_maps(self, map1: Dict[Fraction, str], map2: Dict[Fraction, str]) -> Dict[Fraction, str]:
        """Combine two expression maps using all four operations."""
        result = {}
        for val1, expr1 in map1.items():
            for val2, expr2 in map2.items():
                # addition
                v = val1 + val2
                result[v] = f"({expr1}+{expr2})"
                # absolute subtraction
                v = abs(val1 - val2)
                result[v] = f"abs({expr1}-{expr2})"
                # multiplication
                v = val1 * val2
                result[v] = f"({expr1}*{expr2})"
                # division val1/val2
                if val2 != 0:
                    v = Fraction(val1, val2)
                    result[v] = f"({expr1}/{expr2})"
                # division val2/val1
                if val1 != 0:
                    v = Fraction(val2, val1)
                    result[v] = f"({expr2}/{expr1})"
        return result