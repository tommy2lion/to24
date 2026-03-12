#!/bin/bash
# ============================================================
# Create standard directory structure for a Python library
# Usage: ./create-lib.sh <library-name>
# Example: ./create-lib.sh to24
#   - If name is "to24", generates a full 24-game solver library.
#   - Otherwise, generates a minimal template library.
# Creates a folder named <library-name> in the current directory.
# ============================================================

set -e

if [ -z "$1" ]; then
    echo "❌ Please specify a library name, e.g.: ./create-lib.sh to24"
    exit 1
fi

LIB_NAME="$1"
TARGET_DIR="$(pwd)/$LIB_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "❌ Directory $TARGET_DIR already exists. Choose a different name or delete it first."
    exit 1
fi

echo "📁 Creating library: $LIB_NAME"
echo "   Target directory: $TARGET_DIR"

# Create main project directory
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Create subdirectories: package directory (library_name/), tests/, examples/
mkdir -p "$LIB_NAME" tests examples

# -------------------------------------------------------------------
# Generate files based on library name
# -------------------------------------------------------------------
if [ "$LIB_NAME" = "to24" ]; then
    # ==================== Full to24 library ====================
    # Create algorithm subdirectory
    mkdir -p "$LIB_NAME/algorithm"

    # ----- to24/__init__.py -----
    cat > "$LIB_NAME/__init__.py" << EOF
from .core import To24
from . import algorithm

__all__ = ["To24", "algorithm"]
EOF

    # ----- to24/core.py -----
    cat > "$LIB_NAME/core.py" << 'EOF'
"""
Core module for to24 library.
Provides the main To24 class that dispatches to different algorithms.
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
EOF

    # ----- to24/algorithm/__init__.py -----
    cat > "$LIB_NAME/algorithm/__init__.py" << EOF
from .simple import Simple
from .person_like import PersonLike
from .remove_dup import RemoveDup

__all__ = ["Simple", "PersonLike", "RemoveDup"]
EOF

    # ----- to24/algorithm/simple.py -----
    cat > "$LIB_NAME/algorithm/simple.py" << 'EOF'
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

    def solve(self, a, b, c, d, return_expr=False):
        """
        Try ((a op b) op c) op d pattern.
        """
        nums = [a, b, c, d]
        # basic validation (optional)
        for n in nums:
            if not isinstance(n, int) or n < 1 or n > 10:
                raise ValueError("Numbers must be integers between 1 and 10")

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
EOF

    # ----- to24/algorithm/person_like.py -----
    cat > "$LIB_NAME/algorithm/person_like.py" << 'EOF'
"""
Person-like algorithm (placeholder).
"""

class PersonLike:
    """Placeholder for a human-like reasoning algorithm."""

    def solve(self, a, b, c, d, return_expr=False):
        # TODO: implement actual algorithm
        return (False, "") if return_expr else False
EOF

    # ----- to24/algorithm/remove_dup.py -----
    cat > "$LIB_NAME/algorithm/remove_dup.py" << 'EOF'
"""
Remove duplicate expressions algorithm (placeholder).
"""

class RemoveDup:
    """Placeholder for duplicate removal algorithm."""

    def solve(self, a, b, c, d, return_expr=False):
        # TODO: implement duplicate removal
        return (False, "") if return_expr else False
EOF

    # ----- tests/test.py -----
    cat > tests/test.py << EOF
#!/usr/bin/env python3
import unittest
# If you haven't installed the package, you can uncomment the following lines to add the path manually:
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from $LIB_NAME import To24

class TestTo24(unittest.TestCase):
    def setUp(self):
        self.solver_simple = To24(algorithm='simple')
        self.solver_person = To24(algorithm='person_like')
        self.solver_remove = To24(algorithm='remove_dup')

    def test_simple_known_solutions(self):
        self.assertTrue(self.solver_simple.solve(1, 2, 3, 4))
        self.assertTrue(self.solver_simple.solve(4, 7, 1, 3))
        self.assertTrue(self.solver_simple.solve(6, 6, 6, 6))
        self.assertFalse(self.solver_simple.solve(3, 3, 8, 8))

    def test_simple_no_solution(self):
        self.assertFalse(self.solver_simple.solve(1, 1, 1, 1))

    def test_person_like_placeholder(self):
        self.assertFalse(self.solver_person.solve(1, 2, 3, 4))

    def test_remove_dup_placeholder(self):
        self.assertFalse(self.solver_remove.solve(1, 2, 3, 4))

if __name__ == '__main__':
    unittest.main()
EOF

    # ----- examples/app.py -----
    cat > examples/app.py << EOF
#!/usr/bin/env python3
"""
Simple command-line application to demonstrate to24 library.
"""
import sys
# If you haven't installed the package, you can uncomment the following lines to add the path manually:
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from $LIB_NAME import To24

def main():
    if len(sys.argv) == 5:
        try:
            nums = [int(x) for x in sys.argv[1:5]]
        except ValueError:
            print("Please provide four integers.")
            return
    else:
        nums = [1, 2, 3, 4]

    solver = To24()  # uses default algorithm 'simple'
    result, expr = solver.solve(*nums, return_expr=True)

    if result:
        print(f"{nums} can make 24: {expr}")
    else:
        print(f"{nums} cannot make 24 (using simple algorithm)")

    solver_person = To24(algorithm='person_like')
    result2 = solver_person.solve(*nums)
    print(f"Person-like algorithm result: {result2}")

if __name__ == "__main__":
    main()
EOF

else
    # ==================== Minimal template library ====================
    # ----- library_name/__init__.py -----
    cat > "$LIB_NAME/__init__.py" << EOF
from .core import ${LIB_NAME^}

__all__ = ["${LIB_NAME^}"]
EOF

    # ----- library_name/core.py -----
    cat > "$LIB_NAME/core.py" << EOF
class ${LIB_NAME^}:
    """Example class - rename and modify as needed."""
    
    def __init__(self):
        pass
    
    def example(self):
        return "Hello from $LIB_NAME"
EOF

    # ----- tests/test.py -----
    cat > tests/test.py << EOF
#!/usr/bin/env python3
import unittest
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from $LIB_NAME import ${LIB_NAME^}

class Test${LIB_NAME^}(unittest.TestCase):
    def setUp(self):
        self.obj = ${LIB_NAME^}()

    def test_example(self):
        self.assertEqual(self.obj.example(), "Hello from $LIB_NAME")

if __name__ == '__main__':
    unittest.main()
EOF

    # ----- examples/app.py -----
    cat > examples/app.py << EOF
#!/usr/bin/env python3
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from $LIB_NAME import ${LIB_NAME^}

def main():
    obj = ${LIB_NAME^}()
    print(obj.example())

if __name__ == "__main__":
    main()
EOF

    # Create an empty algorithm directory (optional)
    mkdir -p "$LIB_NAME/algorithm"
    touch "$LIB_NAME/algorithm/__init__.py"
fi

# ----- setup.py -----
cat > setup.py << EOF
from setuptools import setup, find_packages

setup(
    name='$LIB_NAME',
    version='0.1.0',
    packages=find_packages(),
    description='A Python library: $LIB_NAME',
    author='Your Name',
    author_email='your@email.com',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
EOF

# ----- README.md (optional) -----
cat > README.md << EOF
# $LIB_NAME

A Python library.

## Installation

\`\`\`bash
cd $LIB_NAME
pip install -e .
\`\`\`

## Usage

\`\`\`python
from $LIB_NAME import ${LIB_NAME^}
obj = ${LIB_NAME^}()
print(obj.example())
\`\`\`
EOF

echo "✅ Library $LIB_NAME created successfully!"
echo "   Directory structure:"
if command -v tree &> /dev/null; then
    tree -a -F "$TARGET_DIR"
else
    ls -R "$TARGET_DIR"
fi