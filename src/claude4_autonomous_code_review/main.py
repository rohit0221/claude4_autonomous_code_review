"""
Main CLI interface for Claude 4 Autonomous Code Review
"""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

from .claude4_client import Claude4Client
from .config import LOGS_DIR, REPORTS_DIR


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure logging
    log_file = LOGS_DIR / f"claude4_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def save_results(results: dict, output_file: Path = None) -> Path:
    """Save results to JSON file"""
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = REPORTS_DIR / f"claude4_optimization_report_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return output_file


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Claude 4 Autonomous Code Review & Optimization Pipeline"
    )
    
    parser.add_argument(
        "codebase_path",
        type=Path,
        help="Path to the codebase to analyze and optimize"
    )
    
    parser.add_argument(
        "--goals",
        default="Improve code quality, performance, and maintainability",
        help="Optimization goals for the autonomous review"
    )
    
    parser.add_argument(
        "--production",
        action="store_true",
        help="Use Claude 4 Opus with full autonomous capabilities (expensive!)"
    )
    
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum number of autonomous iterations"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for results (default: auto-generated)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    if not args.codebase_path.exists():
        logger.error(f"Codebase path does not exist: {args.codebase_path}")
        return 1
    
    if args.production:
        logger.warning("Using production model (Claude 4 Opus) - this will be expensive!")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            logger.info("Cancelled.")
            return 0
    
    try:
        # Initialize Claude 4 client
        client = Claude4Client(use_production_model=args.production)
        
        logger.info(f"Starting autonomous code review of: {args.codebase_path}")
        logger.info(f"Optimization goals: {args.goals}")
        logger.info(f"Model: {client.model}")
        
        # Run autonomous optimization
        results = client.run_autonomous_code_review(
            codebase_path=args.codebase_path,
            review_goals=args.goals,
            max_iterations=args.max_iterations
        )
        
        # Save results
        output_file = save_results(results, args.output)
        
        # Summary
        logger.info("=" * 60)
        logger.info("AUTONOMOUS CODE REVIEW COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Iterations completed: {len(results['iterations'])}")
        logger.info(f"Total cost estimate: ${results['total_cost_estimate']:.4f}")
        logger.info(f"Duration: {results['total_duration']}")
        logger.info(f"Results saved to: {output_file}")
        
        if "error" in results:
            logger.error(f"Error occurred: {results['error']}")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
