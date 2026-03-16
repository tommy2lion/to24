from .simple import Simple
from .person_like import PersonLike
from .remove_dup import RemoveDup

__all__ = ["Simple", "PersonLike", "RemoveDup"]

from .set_based import SetBasedSolver
__all__ += ["SetBasedSolver"]