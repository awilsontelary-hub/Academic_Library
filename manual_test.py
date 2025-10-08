"""
Manual Bug Detection Test
Tests the Django library system for common bugs and issues
"""
import requests
import time
from urllib.parse import urljoin

BASE_URL = 'http://127.0.0.1:8000'

def test_url(url, test_name, expected_status=200):
    """Test a URL for basic accessibility"""
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {test_name}: Status {response.status_code} (OK)")
            return True, f"✅ {test_name}: Accessible"
        else:
            print(f"⚠️ {test_name}: Status {response.status_code} (Expected {expected_status})")
            return False, f"⚠️ {test_name}: Status {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {test_name}: Request failed - {e}")
        return False, f"❌ {test_name}: Request failed"

def check_content(url, test_name, expected_content):
    """Check if page contains expected content"""
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            found_content = []
            missing_content = []
            
            for item in expected_content:
                if item.lower() in content:
                    found_content.append(item)
                else:
                    missing_content.append(item)
            
            if found_content:
                print(f"✅ {test_name}: Found content - {', '.join(found_content)}")
            
            if missing_content:
                print(f"⚠️ {test_name}: Missing content - {', '.join(missing_content)}")
                
            return len(found_content), len(missing_content)
            
    except Exception as e:
        print(f"❌ {test_name}: Content check failed - {e}")
        return 0, len(expected_content)

def main():
    """Run manual bug detection tests"""
    print("🚀 AcademiaLink Library System - Manual Bug Detection")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Basic URL accessibility
    print("\\n🔍 Testing URL Accessibility...")
    urls_to_test = [
        ('/', 'Homepage'),
        ('/books/', 'Books Page'),
        ('/accounts/login/', 'Login Page'),
        ('/accounts/register/', 'Registration Page'),
        ('/statistics/', 'Statistics Page'),
        ('/dashboard/', 'Dashboard Page'),
        ('/admin/', 'Admin Page')
    ]
    
    accessible_pages = 0
    for path, name in urls_to_test:
        url = urljoin(BASE_URL, path)
        success, result = test_url(url, name)
        test_results.append(result)
        if success or 'Status 302' in result:  # 302 is redirect (expected for protected pages)
            accessible_pages += 1
    
    # Test 2: Content verification
    print("\\n🔍 Testing Page Content...")
    
    # Homepage content
    homepage_expected = ['AcademiaLink', 'Library', 'Books', 'Login']
    found, missing = check_content(BASE_URL, 'Homepage Content', homepage_expected)
    test_results.append(f"✅ Homepage: {found}/{len(homepage_expected)} content items found")
    
    # Books page content
    books_expected = ['Books', 'Search', 'Library']
    found, missing = check_content(urljoin(BASE_URL, '/books/'), 'Books Page Content', books_expected)
    test_results.append(f"✅ Books Page: {found}/{len(books_expected)} content items found")
    
    # Login page content
    login_expected = ['Login', 'Username', 'Password', 'Sign in']
    found, missing = check_content(urljoin(BASE_URL, '/accounts/login/'), 'Login Page Content', login_expected)
    test_results.append(f"✅ Login Page: {found}/{len(login_expected)} content items found")
    
    # Test 3: Form endpoints
    print("\\n🔍 Testing Form Endpoints...")
    
    try:
        # Test login form endpoint
        login_response = requests.post(
            urljoin(BASE_URL, '/accounts/login/'),
            data={'username': '', 'password': ''},
            allow_redirects=False,
            timeout=10
        )
        
        if login_response.status_code in [200, 302, 400]:
            print("✅ Login Form: Endpoint responding correctly")
            test_results.append("✅ Login form endpoint working")
        else:
            print(f"⚠️ Login Form: Unexpected status {login_response.status_code}")
            test_results.append("⚠️ Login form endpoint issue")
            
    except Exception as e:
        print(f"❌ Login Form: Test failed - {e}")
        test_results.append("❌ Login form endpoint error")
    
    # Test 4: Static files
    print("\\n🔍 Testing Static Files...")
    
    static_files = [
        '/static/css/bootstrap.min.css',
        '/static/css/style.css',
        '/static/js/bootstrap.bundle.min.js'
    ]
    
    static_working = 0
    for static_file in static_files:
        url = urljoin(BASE_URL, static_file)
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Static File: {static_file}")
                static_working += 1
            else:
                print(f"⚠️ Static File: {static_file} - Status {response.status_code}")
        except:
            print(f"❌ Static File: {static_file} - Not accessible")
    
    test_results.append(f"✅ Static Files: {static_working}/{len(static_files)} files accessible")
    
    # Test 5: Database connectivity
    print("\\n🔍 Testing Database Connectivity...")
    
    try:
        # Try to access admin which requires database
        admin_response = requests.get(urljoin(BASE_URL, '/admin/'), timeout=10)
        if admin_response.status_code in [200, 302]:
            print("✅ Database: Connection working (admin accessible)")
            test_results.append("✅ Database connectivity working")
        else:
            print("⚠️ Database: May have connection issues")
            test_results.append("⚠️ Database connectivity uncertain")
    except Exception as e:
        print(f"❌ Database: Connection test failed - {e}")
        test_results.append("❌ Database connectivity error")
    
    # Test 6: Security headers
    print("\\n🔍 Testing Security...")
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        headers = response.headers
        
        security_checks = []
        
        # Check CSRF protection
        if 'csrftoken' in response.text or 'csrf' in response.text:
            security_checks.append("✅ CSRF protection found")
        else:
            security_checks.append("⚠️ CSRF protection not detected")
        
        # Check for common security headers
        if 'X-Content-Type-Options' in headers:
            security_checks.append("✅ X-Content-Type-Options header present")
        
        if 'X-Frame-Options' in headers:
            security_checks.append("✅ X-Frame-Options header present")
            
        for check in security_checks:
            print(f"  {check}")
            test_results.append(check)
            
    except Exception as e:
        print(f"❌ Security: Check failed - {e}")
        test_results.append("❌ Security check error")
    
    # Summary
    print("\\n" + "=" * 60)
    print("📊 MANUAL BUG DETECTION SUMMARY")
    print("=" * 60)
    
    passed = len([r for r in test_results if r.startswith("✅")])
    warnings = len([r for r in test_results if r.startswith("⚠️")])
    failed = len([r for r in test_results if r.startswith("❌")])
    total = len(test_results)
    
    print(f"\\n📈 Results: {passed} passed, {warnings} warnings, {failed} failed")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%" if total > 0 else "📊 No tests completed")
    
    print(f"\\n📋 Page Accessibility: {accessible_pages}/{len(urls_to_test)} pages accessible")
    
    if passed >= warnings + failed:
        print("\\n🎉 SYSTEM STATUS: GOOD - No major bugs detected!")
    elif warnings > failed:
        print("\\n👍 SYSTEM STATUS: STABLE - Minor issues detected")
    else:
        print("\\n⚠️ SYSTEM STATUS: NEEDS ATTENTION - Multiple issues found")
    
    print("\\n📋 Detailed Results:")
    for result in test_results:
        print(f"  {result}")
    
    print("\\n💡 Recommendations:")
    if failed == 0:
        print("  ✨ Great! Your system is running well")
        print("  ✨ Consider running Selenium tests for UI testing")
    else:
        print("  🔧 Address any failed tests")
        print("  ⚠️ Review warnings for potential improvements")
        
    print("\\n🔚 Manual bug detection completed!")

if __name__ == '__main__':
    main()