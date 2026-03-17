# think_rules.py
from enum import IntEnum
from typing import Tuple, Dict
from fractions import Fraction

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
        self._impossible_set = {
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
        if key in self._impossible_set:
            return RuleStatus.IMPOSSIBLE, ""
        return RuleStatus.CONTINUE, ""

class Factor4To6Rule(BaseRule):
    """
    Rule: If there is a 4 among the numbers, check if the remaining three can make 6.
    This is a specific instance of the "see N, need M" rule family.
    """
    def __init__(self):
        # Initialize a NumberCombo instance for efficiently checking combinations of three numbers.
        # Note: For better resource sharing, this could be passed in from PersonLike later.
        self._combo = NumberCombo()

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
                results_map = self._combo.three_results_map(*remaining_frac)

                # Check if the target value 6 exists in the results map
                if Fraction(target_result) in results_map:
                    if return_expr:
                        # Build the full expression: 4 * (sub-expression)
                        sub_expr = results_map[Fraction(target_result)]
                        full_expr = f"4 * ({sub_expr})"
                        return RuleStatus.SUCCESS, full_expr
                    return RuleStatus.SUCCESS, ""

        # No matching 4 found, or remaining numbers cannot produce 6
        return RuleStatus.CONTINUE, ""
