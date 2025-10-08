"""
Test Runner Script
Runs all Selenium tests and generates a comprehensive report
"""
import unittest
import sys
import os
import time
from io import StringIO

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(project_root))

class TestResult:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.start_time = time.time()
        self.results = []

def run_test_suite():
    """Run all Selenium test suites"""
    print("🚀 Starting AcademiaLink Library System - Selenium Bug Detection")
    print("=" * 70)
    
    # Import test modules
    try:
        from tests.test_authentication import AuthenticationTests
        from tests.test_library_functionality import LibraryFunctionalityTests
        from tests.test_dashboard_statistics import DashboardStatisticsTests
        from tests.test_ui_accessibility import UIUXAccessibilityTests
    except ImportError as e:
        print(f"❌ Error importing test modules: {e}")
        print("Make sure to install requirements: pip install -r requirements-dev.txt")
        return
    
    # Test suites to run
    test_suites = [
        ('Authentication & Navigation', AuthenticationTests),
        ('Library Functionality', LibraryFunctionalityTests),
        ('Dashboard & Statistics', DashboardStatisticsTests),
        ('UI/UX & Accessibility', UIUXAccessibilityTests)
    ]
    
    overall_result = TestResult()
    
    for suite_name, test_class in test_suites:
        print(f"\\n🔍 Running {suite_name} Tests...")
        print("-" * 50)
        
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        
        # Capture test output
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        
        # Run tests
        result = runner.run(suite)
        
        # Update overall results
        overall_result.total_tests += result.testsRun
        overall_result.passed_tests += (result.testsRun - len(result.failures) - len(result.errors))
        overall_result.failed_tests += len(result.failures)
        overall_result.error_tests += len(result.errors)
        
        # Store suite results
        suite_result = {
            'name': suite_name,
            'total': result.testsRun,
            'passed': result.testsRun - len(result.failures) - len(result.errors),
            'failed': len(result.failures),
            'errors': len(result.errors),
            'failures': result.failures,
            'error_details': result.errors
        }
        overall_result.results.append(suite_result)
        
        # Print suite summary
        if result.wasSuccessful():
            print(f"✅ {suite_name}: ALL TESTS PASSED ({result.testsRun} tests)")
        else:
            print(f"⚠️ {suite_name}: {len(result.failures)} failures, {len(result.errors)} errors")
    
    # Print comprehensive report
    print_final_report(overall_result)

def print_final_report(result):
    """Print comprehensive test report"""
    end_time = time.time()
    duration = end_time - result.start_time
    
    print("\\n" + "=" * 70)
    print("📊 COMPREHENSIVE BUG DETECTION REPORT")
    print("=" * 70)
    
    # Overall statistics
    print(f"\\n⏱️  Total Test Duration: {duration:.2f} seconds")
    print(f"🔢 Total Tests Run: {result.total_tests}")
    print(f"✅ Tests Passed: {result.passed_tests}")
    print(f"❌ Tests Failed: {result.failed_tests}")
    print(f"💥 Test Errors: {result.error_tests}")
    
    # Success rate
    if result.total_tests > 0:
        success_rate = (result.passed_tests / result.total_tests) * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Your system is very stable!")
        elif success_rate >= 70:
            print("👍 GOOD: Minor issues detected, but overall stable")
        elif success_rate >= 50:
            print("⚠️ MODERATE: Several issues need attention")
        else:
            print("🚨 CRITICAL: Major issues detected, requires immediate attention")
    
    # Detailed results by suite
    print("\\n📋 DETAILED RESULTS BY TEST SUITE:")
    print("-" * 50)
    
    for suite_result in result.results:
        status = "✅ PASS" if suite_result['failed'] == 0 and suite_result['errors'] == 0 else "❌ ISSUES"
        print(f"{status} {suite_result['name']}")
        print(f"    Total: {suite_result['total']} | Passed: {suite_result['passed']} | Failed: {suite_result['failed']} | Errors: {suite_result['errors']}")
        
        # Show failure details if any
        if suite_result['failures']:
            print("    Failures:")
            for failure in suite_result['failures']:
                test_name = failure[0].id().split('.')[-1]
                print(f"      - {test_name}")
                
        if suite_result['error_details']:
            print("    Errors:")
            for error in suite_result['error_details']:
                test_name = error[0].id().split('.')[-1]
                print(f"      - {test_name}")
    
    # Recommendations
    print("\\n💡 RECOMMENDATIONS:")
    print("-" * 30)
    
    if result.failed_tests == 0 and result.error_tests == 0:
        print("✨ No issues detected! Your library system is working excellently.")
        print("✨ Consider running these tests regularly during development.")
    else:
        if result.error_tests > 0:
            print("🔧 Fix test errors first - these indicate setup or configuration issues")
        if result.failed_tests > 0:
            print("🐛 Address test failures - these indicate functional bugs")
        print("📚 Review the detailed test output above for specific issues")
        print("🔄 Re-run tests after fixing issues to verify resolution")
    
    print("\\n🔚 Bug detection completed!")
    print("=" * 70)

if __name__ == '__main__':
    # Check if Django server is running
    print("⚠️  IMPORTANT: Make sure your Django server is running on http://127.0.0.1:8000")
    print("   Run: python manage.py runserver")
    print("   Press Enter when server is ready, or Ctrl+C to cancel...")
    
    try:
        input()
        run_test_suite()
    except KeyboardInterrupt:
        print("\\n❌ Test run cancelled by user")
    except Exception as e:
        print(f"\\n💥 Unexpected error: {e}")
        print("Check that all requirements are installed: pip install -r requirements-dev.txt")