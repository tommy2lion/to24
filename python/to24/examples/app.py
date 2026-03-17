#!/usr/bin/env python3
"""
Simple command-line application to demonstrate to24 library.
"""

import sys
import os

# keep next 2 line just for "don't forget debugging history"
# Add the parent directory to path so we can import to24
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from to24 import To24

def main():
    if len(sys.argv) == 5:
        try:
            nums = [int(x) for x in sys.argv[1:5]]
        except ValueError:
            print("Please provide four integers.")
            return
    else:
        # Default test case
        nums = [1, 2, 3, 4]

    solver = To24()  # uses default algorithm 'simple'
    result, expr = solver.solve(*nums, return_expr=True)

    if result:
        print(f"{nums} can make 24: {expr}")
    else:
        print(f"{nums} cannot make 24 (using simple algorithm)")

    # Set-based algorithm
    solver_set = To24(algorithm='set_based')
    result3, expr3 = solver_set.solve(*nums, return_expr=True)
    if result3:
        print(f"Set-based algorithm: {nums} can make 24: {expr3}")
    else:
        print(f"Set-based algorithm: {nums} cannot make 24")


    # Try different algorithm
    solver_person = To24(algorithm='person_like')
    result2, expr2 = solver_set.solve(*nums, return_expr=True)
    if result2:
        print(f"Person-like algorithm: {nums} can make 24: {expr2}")
    else:
        print(f"Person-like algorithm: {nums} cannot make 24")

if __name__ == "__main__":
    main()