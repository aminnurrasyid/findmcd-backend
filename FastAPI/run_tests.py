#!/usr/bin/env python3
"""
Test runner script for the fetch outlet endpoint tests

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --performance      # Run only performance tests
    python run_tests.py --edge-case        # Run only edge case tests
    python run_tests.py --coverage         # Run tests with coverage report
"""

import sys
import subprocess
import argparse
import os


def run_command(cmd):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run fetch outlet endpoint tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--edge-case", action="store_true", help="Run edge case tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--file", "-f", help="Run specific test file")
    
    args = parser.parse_args()
    
    # Change to the FastAPI directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-vv")
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term-missing"])
    
    # Add specific markers if requested
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.performance:
        cmd.extend(["-m", "performance"])
    elif args.edge_case:
        cmd.extend(["-m", "edge_case"])
    
    # Add specific file if requested
    if args.file:
        cmd.append(args.file)
    else:
        cmd.append("tests/test_fetch_outlet.py")
    
    # Run the tests
    return_code = run_command(cmd)
    
    if return_code == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())