"""
Configuration settings for Claude 4 Autonomous Code Review
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Development vs Production models
DEVELOPMENT_MODEL = "claude-3-haiku-20240307"  # Cheapest for testing
PRODUCTION_MODEL = "claude-4-opus"             # Full autonomous capabilities

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
SRC_DIR = PROJECT_ROOT / "src"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Model settings
MAX_TOKENS = 4096
TEMPERATURE = 0.1  # Low for consistent code analysis

# Autonomous workflow settings
MAX_ITERATIONS = 50  # Prevent infinite loops
SESSION_TIMEOUT = 3600  # 1 hour for development, 7 hours for production
