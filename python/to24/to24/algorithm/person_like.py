# person_like.py
from typing import List
from .think_rules import BaseRule, RuleStatus, AddAllRule, MultiplyAllRule, SpecialFractionRule, NoSolutionRule

class PersonLike:
    """
    Human‑like solver that tries a sequence of heuristic rules,
    falling back to the simple brute‑force solver if none succeed.
    """

    def __init__(self):
        # Rule list in order of priority.
        self.rules: List[BaseRule] = [
            NoSolutionRule(),               # fast fail for known unsolvable
            SpecialFractionRule(),           # memorized classic fraction solutions
            AddAllRule(),
            MultiplyAllRule(),
            # More rules will be added later...
        ]

    def solve(self, a: int, b: int, c: int, d: int, return_expr: bool = False):
        """
        Try each rule; if any returns SUCCESS, return the result.
        If any returns IMPOSSIBLE, return no solution immediately.
        Otherwise fall back to Simple.
        """
        for rule in self.rules:
            status, expr = rule.apply(a, b, c, d, return_expr)
            if status == RuleStatus.SUCCESS:
                if return_expr:
                    return True, expr
                return True
            elif status == RuleStatus.IMPOSSIBLE:
                return (False, "") if return_expr else False
            # CONTINUE: try next rule

        # Fallback to the complete simple algorithm
        from .simple import Simple
        simple = Simple()
        return simple.solve(a, b, c, d, return_expr)
