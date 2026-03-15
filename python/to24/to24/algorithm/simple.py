"""
Complete 24-game solver, enumerating all permutations, operators, and five parentheses patterns.
"""

import itertools
from itertools import permutations, product

class Simple:
    """Complete brute-force solver capable of finding all possible expressions."""

    def __init__(self):
        # List of operator symbols used to generate expressions
        self.op_symbols = ['+', '-', '*', '/']

    def _check_numbers(self, a, b, c, d):
        """Validate that input numbers are integers between 1 and 10."""
        nums = [a, b, c, d]
        for n in nums:
            if not isinstance(n, int):
                raise TypeError(f"Arguments must be integers, got {type(n).__name__}")
            if n < 1 or n > 10:
                raise ValueError(f"Arguments must be between 1 and 10, got {n}")
        return tuple(nums)

    def solve(self, a, b, c, d, return_expr=False):
        """
        Determine whether four numbers can yield 24 using +, -, *, /.
        :param a,b,c,d: four integers (1-10)
        :param return_expr: if True, also return a valid expression
        :return: bool if return_expr=False, otherwise (bool, str)
        """
        nums = self._check_numbers(a, b, c, d)

        # Five parentheses pattern templates (eval-safe because only numbers and operators are used)
        templates = [
            '(({0}{4}{1}){5}{2}){6}{3}',   # ((a op b) op c) op d
            '({0}{4}{1}){5}({2}{6}{3})',   # (a op b) op (c op d)
            '({0}{4}({1}{5}{2})){6}{3}',   # (a op (b op c)) op d
            '{0}{4}(({1}{5}{2}){6}{3})',   # a op ((b op c) op d)
            '{0}{4}({1}{5}({2}{6}{3}))'    # a op (b op (c op d))
        ]

        # Generate all distinct permutations of the numbers
        perms = set(permutations(nums))

        for a_perm in perms:
            a, b, c, d = a_perm
            # Generate all operator combinations
            for ops in product(self.op_symbols, repeat=3):
                op1, op2, op3 = ops
                for template in templates:
                    # Build the expression string
                    expr = template.format(a, b, c, d, op1, op2, op3)
                    try:
                        # Evaluate the expression, taking floating-point tolerance into account
                        if abs(eval(expr) - 24) < 1e-6:
                            if return_expr:
                                return True, expr
                            return True
                    except ZeroDivisionError:
                        continue
                    except Exception:
                        # Ignore any other exceptions (e.g., syntax errors)
                        continue

        return (False, "") if return_expr else False


if __name__ == "__main__":
    solver = Simple()
    test_cases = [
        (1, 2, 3, 4),
        (3, 3, 8, 8),
        (4, 4, 4, 4),
        (1, 1, 1, 1),
        (6, 6, 6, 6),
        (5, 5, 5, 1),
    ]

    for a, b, c, d in test_cases:
        found, expr = solver.solve(a, b, c, d, return_expr=True)
        if found:
            print(f"{a} {b} {c} {d} -> {expr}")
        else:
            print(f"{a} {b} {c} {d} -> No solution")