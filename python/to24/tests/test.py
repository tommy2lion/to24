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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from to24 import To24
# print(to24.__file__) 

class TestTo24(unittest.TestCase):
    def setUp(self):
        self.solver_simple = To24(algorithm='simple')
        self.solver_person = To24(algorithm='person_like')
        self.solver_remove = To24(algorithm='remove_dup')

    def test_simple_known_solutions(self):
        self.assertTrue(self.solver_simple.solve(1, 2, 3, 4))
        self.assertTrue(self.solver_simple.solve(4, 7, 1, 3))
        self.assertTrue(self.solver_simple.solve(6, 6, 6, 6))
        # 3,3,8,8 is solvable but not by simple pattern
        self.assertFalse(self.solver_simple.solve(3, 3, 8, 8))

    def test_simple_no_solution(self):
        self.assertFalse(self.solver_simple.solve(1, 1, 1, 1))

    def test_person_like_placeholder(self):
        # Placeholder returns False
        self.assertFalse(self.solver_person.solve(1, 2, 3, 4))

    def test_remove_dup_placeholder(self):
        self.assertFalse(self.solver_remove.solve(1, 2, 3, 4))

if __name__ == '__main__':
    unittest.main()