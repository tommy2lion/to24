"""
Simple brute-force algorithm for 24-game.
Enumerates all permutations and operator combinations with a fixed parentheses pattern.
"""

import itertools
import operator

class Simple:
    """Simple brute-force solver."""

    def __init__(self):
        self.ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

    def _check_numbers(self, a, b, c, d):
        nums = [a, b, c, d]
        for n in nums:
            if not isinstance(n, int):
                raise TypeError(f"Arguments must be integers, got {type(n).__name__}")
            if n < 1 or n > 10:
                raise ValueError(f"Arguments must be between 1 and 10, got {n}")
        return tuple(nums)

    def solve(self, a, b, c, d, return_expr=False):
        """
        Try ((a op b) op c) op d pattern.
        """
        nums = self._check_numbers(a, b, c, d)

        for perm in set(itertools.permutations(nums)):
            for ops in itertools.product(self.ops.keys(), repeat=3):
                try:
                    val = self.ops[ops[0]](perm[0], perm[1])
                    val = self.ops[ops[1]](val, perm[2])
                    val = self.ops[ops[2]](val, perm[3])
                    if abs(val - 24) < 1e-6:
                        if return_expr:
                            expr = f"(({perm[0]} {ops[0]} {perm[1]}) {ops[1]} {perm[2]}) {ops[2]} {perm[3]}"
                            return True, expr
                        return True
                except ZeroDivisionError:
                    continue

        return (False, "") if return_expr else False

if __name__ == "__main__":
    solver = Simple()
    test_cases = [
        (1, 2, 3, 4),
        (4, 7, 1, 3),
        (6, 6, 6, 6),
        (3, 3, 8, 8),
    ]
    for a, b, c, d in test_cases:
        result, expr = solver.solve(a, b, c, d, return_expr=True)
        if result:
            print(f"{a} {b} {c} {d} -> can got 24: {expr}")
        else:
            print(f"{a} {b} {c} {d} -> can't got 24 with simple algorithm")

            