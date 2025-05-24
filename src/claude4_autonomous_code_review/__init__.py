"""
Clean Iterative Code Review System
Single implementation, no duplicates, generates JSON + Markdown
"""

__version__ = "3.0.0"
__all__ = [
    "CleanIterativeReviewer",
    "human_review_and_apply_fixes"
]

# Clean imports
from .clean_review import CleanIterativeReviewer, human_review_and_apply_fixes
from .config import DEVELOPMENT_MODEL, PRODUCTION_MODEL, REPORTS_DIR
