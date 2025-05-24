"""
Configuration settings for Iterative Code Review
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model configuration
DEVELOPMENT_MODEL = "claude-3-haiku-20240307"  # Cheap for testing ($0.25/$1.25 per million tokens)
PRODUCTION_MODEL = "claude-4-opus"             # Expensive but powerful ($15/$75 per million tokens)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY not found in environment variables.")
    print("Please create a .env file in the project root with:")
    print("ANTHROPIC_API_KEY=your_actual_api_key_here")
    print("")
    ANTHROPIC_API_KEY = input("Enter your Anthropic API key now: ").strip()
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY is required to proceed")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure directories exist
REPORTS_DIR.mkdir(exist_ok=True)

# Model settings
MAX_TOKENS = 4096
TEMPERATURE = 0.1  # Low for consistent code analysis

# Iterative review settings
DEFAULT_ITERATIONS = 5  # Default number of iterations for testing
