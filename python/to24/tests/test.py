#!/usr/bin/env python3
"""
Unit tests for to24 library.
"""

# 下面是刚才加的测试代码
# import sys
# print("sys.path =", sys.path)
# import to24
# print("to24 =", to24)
# print("type(to24) =", type(to24))
# print("to24.__file__ =", getattr(to24, "__file__", "No __file__"))

# 这是原始的import
import sys
import os
import unittest

# keep next line for debugging
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from to24 import To24
# print(to24.__file__) 

from to24.algorithm.set_based import SetBased

class TestTo24(unittest.TestCase):
    def setUp(self):
        self.solver_simple = To24(algorithm='simple')
        self.solver_person = To24(algorithm='person_like')
        self.solver_remove = To24(algorithm='remove_dup')

    def test_simple_known_solutions(self):
        self.assertTrue(self.solver_simple.solve(1, 2, 3, 4))
        self.assertTrue(self.solver_simple.solve(4, 7, 1, 3))
        self.assertTrue(self.solver_simple.solve(6, 6, 6, 6))
        self.assertTrue(self.solver_simple.solve(3, 3, 8, 8))

    def test_simple_no_solution(self):
        self.assertFalse(self.solver_simple.solve(1, 1, 1, 1))

    def test_person_like_rules(self):
        solver = To24(algorithm='person_like')
        # Should succeed via special fraction rule
        self.assertTrue(solver.solve(5, 5, 5, 1))
        self.assertTrue(solver.solve(3, 3, 8, 8))
        # Should succeed via add all rule
        self.assertTrue(solver.solve(1, 2, 3, 4))
        # No solution
        self.assertFalse(solver.solve(1, 1, 1, 1))

    def test_remove_dup_placeholder(self):
        self.assertFalse(self.solver_remove.solve(1, 2, 3, 4))

    def test_set_based_solver(self):
        solver = SetBased()
        self.assertTrue(solver.solve(1, 2, 3, 4))
        self.assertTrue(solver.solve(3, 3, 8, 8))  # classic dilemma
        self.assertFalse(solver.solve(1, 1, 1, 1))
        ok, expr = solver.solve(5, 5, 5, 1, return_expr=True)
        self.assertTrue(ok)
        self.assertAlmostEqual(eval(expr), 24)  # use assertAlmostEqual to avoid floating-point errors

    def test_set_based_solver_expression(self):
        solver = SetBased()
        test_cases = [
            (1, 2, 3, 4),
            (3, 3, 8, 8),
            (5, 5, 5, 1),
            (4, 4, 4, 4),
            (6, 6, 6, 6),
            (1, 1, 1, 1),  # no solution, should return False and an empty string
        ]
        for a, b, c, d in test_cases:
            ok, expr = solver.solve(a, b, c, d, return_expr=True)
            if ok:
                # verify - the expression evaluates should be 24
                from fractions import Fraction
                print(f"Expression for ({a},{b},{c},{d}): {expr}")
                # self.assertEqual(eval(expr), Fraction(24))
                # self.assertAlmostEqual(eval(expr), 24, places=12)
                self.assertAlmostEqual(eval(expr), 24, delta=1e-9)
            else:
                self.assertEqual(expr, "")

 
if __name__ == '__main__':
    unittest.main()