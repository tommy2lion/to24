# think_rules.py
from enum import IntEnum
from typing import Tuple, Dict, Optional
from fractions import Fraction
from .combo_cache import NumberCombo


class RuleStatus(IntEnum):
    """Result status for rule application."""
    SUCCESS = 0      # Rule found a solution
    IMPOSSIBLE = 1   # Rule determined no solution exists (stop trying)
    CONTINUE = 2     # Rule does not apply, try next rule

class BaseRule:
    """Base class for all rules. Each rule must implement apply()."""
    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        """
        Apply the rule to the four numbers.
        Returns (status, expression). If return_expr is False, expression may be empty.
        """
        raise NotImplementedError

class AddAllRule(BaseRule):
    """Rule: a + b + c + d == 24."""
    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        if a + b + c + d == 24:
            if return_expr:
                return RuleStatus.SUCCESS, f"{a}+{b}+{c}+{d}"
            return RuleStatus.SUCCESS, ""
        return RuleStatus.CONTINUE, ""

class MultiplyAllRule(BaseRule):
    """Rule: a * b * c * d == 24."""
    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        if a * b * c * d == 24:
            if return_expr:
                return RuleStatus.SUCCESS, f"{a}*{b}*{c}*{d}"
            return RuleStatus.SUCCESS, ""
        return RuleStatus.CONTINUE, ""

class SpecialFractionRule(BaseRule):
    """
    Rule: lookup table for classic fraction solutions that involve division,
    such as (5,5,5,1) -> "5*(5-1/5)".
    """
    def __init__(self):
        # Keys are sorted tuples of the four numbers.
        self._specials: Dict[Tuple[int, int, int, int], str] = {
            (1,5,5,5): "5*(5-1/5)",
            (3,3,7,7): "7*(3+3/7)",
            (3,3,8,8): "8/(3-8/3)",
            (4,4,7,7): "7*(4-4/7)",
            (1,3,4,6): "6/(1-3/4)",    # 6/(1-3/4)=24
            (1,4,5,6): "4/(1-5/6)",
            (1,6,6,8): "6/(1-6/8)",    # 6/(1-6/8)=24
        }

    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        key = tuple(sorted((a, b, c, d)))
        if key in self._specials:
            expr = self._specials[key]
            if return_expr:
                return RuleStatus.SUCCESS, expr
            return RuleStatus.SUCCESS, ""
        return RuleStatus.CONTINUE, ""

class NoSolutionRule(BaseRule):
    """
    Rule: if the four numbers are in a precomputed set of impossible combinations,
    return IMPOSSIBLE immediately (no solution).
    """
    def __init__(self):
        # Hardcoded set of unsolvable combinations (sorted tuples)
        self._no_solution_set = {
            (1,1,1,1),
            (2,2,2,2),
            (7,7,7,7),
            (8,8,8,8),
            (9,9,9,9),
            (10,10,10,10),
            # Add more as needed
        }

    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        key = tuple(sorted((a, b, c, d)))
        if key in self._no_solution_set:
            return RuleStatus.IMPOSSIBLE, ""
        return RuleStatus.CONTINUE, ""

class Factor4To6Rule(BaseRule):
    """
    Rule: If there is a 4 among the numbers, check if the remaining three can make 6.
    This is a specific instance of the "see N, need M" rule family.
    Uses a shared NumberCombo cache for efficiency.
    """
    def __init__(self, combo: NumberCombo):
        self._combo = combo   # use the shared cache

    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        numbers = [a, b, c, d]
        target_factor = 4
        target_result = 6

        # Iterate through all numbers to find the one equal to 4
        for i in range(4):
            if numbers[i] == target_factor:
                # Get the remaining three numbers
                remaining = numbers[:i] + numbers[i+1:]

                # Convert remaining numbers to Fraction and obtain their result-to-expression map
                remaining_frac = [Fraction(x) for x in remaining]
                # Get the expression map for the three numbers
                results_map = self._combo.three_results_map(*remaining_frac)
                target = Fraction(target_result)

                # Check if the target value 6 exists in the results map
                if target in results_map:
                    if return_expr:
                        # Build the full expression: 4 * (sub-expression)
                        sub_expr = results_map[target]
                        full_expr = f"4 * ({sub_expr})"
                        return RuleStatus.SUCCESS, full_expr
                    return RuleStatus.SUCCESS, ""

        # No matching 4 found, or remaining numbers cannot produce 6
        return RuleStatus.CONTINUE, ""

class Factor6To4Rule(BaseRule):
    """
    Rule: If there is a 6 among the numbers, check if the remaining three can make 4.
    This is another instance of the "see N, need M" rule family.
    Uses a shared NumberCombo cache for efficiency.
    """
    def __init__(self, combo: NumberCombo):
        self._combo = combo

    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        numbers = [a, b, c, d]
        target_factor = 6
        target_result = 4

        for i in range(4):
            if numbers[i] == target_factor:
                remaining = numbers[:i] + numbers[i+1:]
                remaining_frac = [Fraction(x) for x in remaining]
                results_map = self._combo.three_results_map(*remaining_frac)
                target = Fraction(target_result)

                if target in results_map:
                    if return_expr:
                        sub_expr = results_map[target]
                        full_expr = f"6 * ({sub_expr})"
                        return RuleStatus.SUCCESS, full_expr
                    return RuleStatus.SUCCESS, ""

        return RuleStatus.CONTINUE, ""

class Pair6And4Rule(BaseRule):
    """
    Rule: Try to split the four numbers into two pairs such that one pair makes 6 and the other makes 4,
    then combine them with multiplication to get 24.
    Uses NumberCombo cache to check pair results efficiently.
    """
    def __init__(self, combo: NumberCombo):
        self._combo = combo

    def apply(self, a: int, b: int, c: int, d: int, return_expr: bool = False) -> Tuple[RuleStatus, str]:
        nums = [a, b, c, d]
        # All possible unordered pairings (3 ways)
        pairings = [
            ((0,1), (2,3)),  # (a,b) and (c,d)
            ((0,2), (1,3)),  # (a,c) and (b,d)
            ((0,3), (1,2))   # (a,d) and (b,c)
        ]
        target1 = 6
        target2 = 4
        target_frac1 = Fraction(target1)
        target_frac2 = Fraction(target2)

        for idx1, idx2 in pairings:
            # Pair 1
            p1_vals = [nums[i] for i in idx1]
            p2_vals = [nums[i] for i in idx2]
            # Get result maps for both pairs
            map1 = self._combo.two_results_map(Fraction(p1_vals[0]), Fraction(p1_vals[1]))
            map2 = self._combo.two_results_map(Fraction(p2_vals[0]), Fraction(p2_vals[1]))

            # Check if (map1 has 6 and map2 has 4) OR (map1 has 4 and map2 has 6)
            if target_frac1 in map1 and target_frac2 in map2:
                if return_expr:
                    expr1 = map1[target_frac1]
                    expr2 = map2[target_frac2]
                    full_expr = f"({expr1}) * ({expr2})"
                    return RuleStatus.SUCCESS, full_expr
                return RuleStatus.SUCCESS, ""
            if target_frac2 in map1 and target_frac1 in map2:
                if return_expr:
                    expr1 = map1[target_frac2]
                    expr2 = map2[target_frac1]
                    full_expr = f"({expr1}) * ({expr2})"
                    return RuleStatus.SUCCESS, full_expr
                return RuleStatus.SUCCESS, ""

        return RuleStatus.CONTINUE, ""

