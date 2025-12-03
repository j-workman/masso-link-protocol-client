#!/usr/bin/env python3
"""
Test runner for MASSO UDP Client

Runs all test suites and provides summary.
"""

import sys
import os
import time
import subprocess

def run_test_file(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Only show stdout, hide stderr since it's just test details
        print(result.stdout)
        
        # Add delay after real controller tests to let controller recover
        if test_file == 'test_real_controller.py' and result.returncode == 0:
            print("\n[*] Waiting 3 seconds for controller to recover...")
            time.sleep(3)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all test suites"""
    print("MASSO UDP Client - Complete Test Suite")
    print("=" * 60)
    
    # Optional delay between test files (in seconds)
    delay_between_tests = 0  # Set to >0 to add delays
    
    test_files = [
        'test_simple.py',      # Basic functionality tests
        'test_masso_client.py', # Comprehensive unit tests
        'test_real_controller.py', # Real controller integration tests (run last)
    ]
    
    results = {}
    
    for i, test_file in enumerate(test_files):
        if os.path.exists(test_file):
            results[test_file] = run_test_file(test_file)
            
            # Add delay between test files (except after the last one)
            if delay_between_tests > 0 and i < len(test_files) - 1:
                print(f"\n[*] Waiting {delay_between_tests} seconds before next test suite...")
                time.sleep(delay_between_tests)
        else:
            print(f"Warning: {test_file} not found")
            results[test_file] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_file, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_file:<25} : {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
