"""
Core module for to24 library.
Provides the main to24 class that dispatches to different algorithms.
"""

import importlib

class To24:
    """24-game solver with pluggable algorithms."""

    def __init__(self, algorithm="simple"):
        """
        Initialize solver with specified algorithm.
        
        :param algorithm: Name of algorithm module (e.g., 'simple', 'person_like', 'remove_dup')
        """
        self.algorithm_name = algorithm
        self._solver = None

    def _get_solver(self):
        """Lazy load the solver module."""
        if self._solver is None:
            try:
                module = importlib.import_module(f"to24.algorithm.{self.algorithm_name}")
                # Assume each module defines a class with the same name (capitalized)
                class_name = ''.join(x.capitalize() for x in self.algorithm_name.split('_'))
                solver_class = getattr(module, class_name)
                self._solver = solver_class()
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Algorithm '{self.algorithm_name}' not found or invalid") from e
        return self._solver

    def solve(self, a, b, c, d, return_expr=False):
        """
        Check if four numbers can make 24 using selected algorithm.
        
        :param a,b,c,d: integers between 1 and 10
        :param return_expr: if True, return (bool, expression)
        :return: bool or (bool, str)
        """
        solver = self._get_solver()
        return solver.solve(a, b, c, d, return_expr)
    
if __name__ == "__main__":
    from algorithm.simple import Simple  # Note: When running core.py directly, algorithm is in the same directory level
    solver = Simple()
    test = (1, 2, 3, 4)
    result, expr = solver.solve(*test, return_expr=True)
    if result:
        print(f"core.py test: {test} -> {expr}")
    else:
        print(f"core.py test: {test} -> no solution")
