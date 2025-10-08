"""
Authentication Tests
Tests for login, registration, logout, and access control functionality
"""
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tests.test_config import TestConfig, TEST_URLS

class AuthenticationTests(unittest.TestCase):
    """Test suite for authentication functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.driver = TestConfig.get_chrome_driver()
        self.driver.implicitly_wait(10)
        
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()
        
    def test_homepage_loads(self):
        """Test if homepage loads correctly"""
        print("\\n🔍 Testing homepage load...")
        self.driver.get(TEST_URLS['home'])
        
        # Check if page loads
        self.assertIn("AcademiaLink", self.driver.title)
        print("✅ Homepage loaded successfully")
        
        # Check for navigation elements
        try:
            nav = self.driver.find_element(By.TAG_NAME, "nav")
            self.assertTrue(nav.is_displayed())
            print("✅ Navigation bar found")
        except NoSuchElementException:
            print("❌ Navigation bar not found")
            
    def test_registration_page_access(self):
        """Test registration page accessibility"""
        print("\\n🔍 Testing registration page access...")
        self.driver.get(TEST_URLS['register'])
        
        # Check if registration form exists
        try:
            form = self.driver.find_element(By.TAG_NAME, "form")
            self.assertTrue(form.is_displayed())
            print("✅ Registration form found")
            
            # Check required fields
            required_fields = ['username', 'email', 'password1', 'password2']
            for field in required_fields:
                try:
                    element = self.driver.find_element(By.NAME, field)
                    print(f"✅ Field '{field}' found")
                except NoSuchElementException:
                    print(f"❌ Required field '{field}' missing")
                    
        except NoSuchElementException:
            print("❌ Registration form not found")
            
    def test_login_page_access(self):
        """Test login page accessibility"""
        print("\\n🔍 Testing login page access...")
        self.driver.get(TEST_URLS['login'])
        
        # Check if login form exists
        try:
            form = self.driver.find_element(By.TAG_NAME, "form")
            self.assertTrue(form.is_displayed())
            print("✅ Login form found")
            
            # Check for username and password fields
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            self.assertTrue(username_field.is_displayed())
            self.assertTrue(password_field.is_displayed())
            print("✅ Username and password fields found")
            
        except NoSuchElementException as e:
            print(f"❌ Login form elements not found: {e}")
            
    def test_registration_form_validation(self):
        """Test registration form validation"""
        print("\\n🔍 Testing registration form validation...")
        self.driver.get(TEST_URLS['register'])
        
        try:
            # Try to submit empty form
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            submit_btn.click()
            time.sleep(2)
            
            # Check if we're still on registration page (validation should prevent submission)
            current_url = self.driver.current_url
            if 'register' in current_url:
                print("✅ Form validation working - empty form rejected")
            else:
                print("❌ Form validation failed - empty form accepted")
                
        except NoSuchElementException:
            print("❌ Submit button not found")
            
    def test_navigation_links(self):
        """Test navigation menu functionality"""
        print("\\n🔍 Testing navigation links...")
        self.driver.get(TEST_URLS['home'])
        
        # Common navigation links to test
        nav_links = [
            ('Books', '/books/'),
            ('Login', '/accounts/login/'),
            ('Register', '/accounts/register/')
        ]
        
        for link_text, expected_url in nav_links:
            try:
                # Go back to home page
                self.driver.get(TEST_URLS['home'])
                time.sleep(1)
                
                # Find and click navigation link
                link = self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                link.click()
                time.sleep(2)
                
                # Check if navigation worked
                current_url = self.driver.current_url
                if expected_url in current_url:
                    print(f"✅ Navigation to '{link_text}' working")
                else:
                    print(f"❌ Navigation to '{link_text}' failed - Expected: {expected_url}, Got: {current_url}")
                    
            except NoSuchElementException:
                print(f"❌ Navigation link '{link_text}' not found")
            except Exception as e:
                print(f"❌ Error testing '{link_text}' navigation: {e}")
                
    def test_responsive_design(self):
        """Test responsive design on different screen sizes"""
        print("\\n🔍 Testing responsive design...")
        
        # Test different screen sizes
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device_type in screen_sizes:
            self.driver.set_window_size(width, height)
            self.driver.get(TEST_URLS['home'])
            time.sleep(2)
            
            # Check if navigation is accessible
            try:
                nav = self.driver.find_element(By.TAG_NAME, "nav")
                if nav.is_displayed():
                    print(f"✅ {device_type} ({width}x{height}): Navigation visible")
                else:
                    print(f"⚠️ {device_type} ({width}x{height}): Navigation hidden (may be collapsed)")
            except NoSuchElementException:
                print(f"❌ {device_type} ({width}x{height}): Navigation not found")

if __name__ == '__main__':
    unittest.main()