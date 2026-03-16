# combo_cache.py
from fractions import Fraction
from typing import Dict, Tuple
from .set_ops import combine

class NumberCombo:
    """
    Caches results for two and three numbers, including an example expression for each value.
    """

    def __init__(self):
        # Cache for two numbers: maps sorted pair to {value: example_expression}
        self._two_expr: Dict[Tuple[Fraction, Fraction], Dict[Fraction, str]] = {}
        # Cache for three numbers: maps sorted triple to {value: example_expression}
        self._three_expr: Dict[Tuple[Fraction, Fraction, Fraction], Dict[Fraction, str]] = {}

    def two_results_map(self, a: Fraction, b: Fraction) -> Dict[Fraction, str]:
        """
        Returns a dictionary mapping each possible result of combining a and b
        to an example expression that yields that result.
        """
        key = tuple(sorted([a, b]))
        if key in self._two_expr:
            return self._two_expr[key]

        x, y = key
        expr_map = {}

        # addition
        val = x + y
        expr_map[val] = f"({x}+{y})"

        # absolute subtraction (covers both orders)
        val = abs(x - y)
        if val not in expr_map:  # avoid overwriting if e.g. x-y = y-x = 0
            expr_map[val] = f"abs({x}-{y})"

        # multiplication
        val = x * y
        expr_map[val] = f"({x}*{y})"

        # division a/b
        if y != 0:
            val = Fraction(x, y)
            expr_map[val] = f"({x}/{y})"

        # division b/a
        if x != 0:
            val = Fraction(y, x)
            expr_map[val] = f"({y}/{x})"

        self._two_expr[key] = expr_map
        return expr_map

    def three_results_map(self, a: Fraction, b: Fraction, c: Fraction) -> Dict[Fraction, str]:
        """
        Returns a dictionary mapping each possible result of combining a, b, c
        to an example expression.
        """
        key = tuple(sorted([a, b, c]))
        if key in self._three_expr:
            return self._three_expr[key]

        x, y, z = key
        expr_map = {}

        # Helper to combine two maps (like a binary operation)
        def combine_maps(map1: Dict[Fraction, str], map2: Dict[Fraction, str]) -> Dict[Fraction, str]:
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

        # Three possible binary tree structures:
        # 1. (x op y) op z
        map_xy = self.two_results_map(x, y)
        # combine map_xy with {z} (single element map)
        map_z = {z: str(z)}
        map1 = combine_maps(map_xy, map_z)
        expr_map.update(map1)

        # 2. (x op z) op y
        map_xz = self.two_results_map(x, z)
        map_y = {y: str(y)}
        map2 = combine_maps(map_xz, map_y)
        expr_map.update(map2)

        # 3. (y op z) op x
        map_yz = self.two_results_map(y, z)
        map_x = {x: str(x)}
        map3 = combine_maps(map_yz, map_x)
        expr_map.update(map3)

        self._three_expr[key] = expr_map
        return expr_map