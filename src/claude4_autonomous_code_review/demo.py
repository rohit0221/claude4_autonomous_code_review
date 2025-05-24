"""
Example script demonstrating Claude 4 autonomous capabilities
"""
import os
from pathlib import Path

from claude4_autonomous_code_review.claude4_client import Claude4Client
from claude4_autonomous_code_review.config import REPORTS_DIR


def demo_autonomous_review():
    """
    Demo the autonomous code review on this project itself
    """
    # Set your API key
    os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"
    
    # Initialize with development model (cheap for testing)
    client = Claude4Client(use_production_model=False)
    
    # Use this project as the target for review
    project_path = Path(__file__).parent
    
    # Run autonomous optimization
    results = client.run_autonomous_optimization(
        codebase_path=project_path,
        optimization_goals="Improve code structure, add error handling, and enhance documentation",
        max_iterations=5
    )
    
    print("Autonomous review completed!")
    print(f"Iterations: {len(results['iterations'])}")
    print(f"Cost estimate: ${results['total_cost_estimate']:.4f}")
    
    return results


if __name__ == "__main__":
    demo_autonomous_review()
