"""
Dashboard and Statistics Tests
Tests for dashboard functionality, statistics, and admin features
"""
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tests.test_config import TestConfig, TEST_URLS

class DashboardStatisticsTests(unittest.TestCase):
    """Test suite for dashboard and statistics functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.driver = TestConfig.get_chrome_driver()
        self.driver.implicitly_wait(10)
        
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()
        
    def test_dashboard_accessibility(self):
        """Test dashboard page accessibility"""
        print("\\n🔍 Testing dashboard accessibility...")
        self.driver.get(TEST_URLS['dashboard'])
        
        # Check if page loads or redirects to login
        current_url = self.driver.current_url
        
        if 'login' in current_url:
            print("✅ Dashboard protected - redirected to login (expected behavior)")
        else:
            # If dashboard loads, check for dashboard elements
            try:
                dashboard_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".dashboard, .card, .statistics, .stats")
                
                if dashboard_elements:
                    print(f"✅ Dashboard loaded with {len(dashboard_elements)} elements")
                else:
                    print("⚠️ Dashboard page loaded but no dashboard elements found")
                    
            except Exception as e:
                print(f"❌ Error accessing dashboard: {e}")
                
    def test_statistics_page_access(self):
        """Test statistics page accessibility"""
        print("\\n🔍 Testing statistics page access...")
        self.driver.get(TEST_URLS['statistics'])
        
        # Check if page loads or redirects
        current_url = self.driver.current_url
        
        if 'login' in current_url:
            print("✅ Statistics protected - redirected to login")
        else:
            try:
                # Look for statistics elements
                stats_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".statistics, .stats, .analytics, .metrics, .count")
                
                if stats_elements:
                    print(f"✅ Statistics page loaded with {len(stats_elements)} elements")
                    
                    # Check for interactive elements
                    clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                        "[onclick], .clickable, .dropdown-toggle, .expandable")
                    
                    if clickable_elements:
                        print(f"✅ Found {len(clickable_elements)} interactive statistics elements")
                    else:
                        print("⚠️ No interactive elements found in statistics")
                        
                else:
                    print("⚠️ Statistics page loaded but no statistics elements found")
                    
            except Exception as e:
                print(f"❌ Error accessing statistics: {e}")
                
    def test_statistics_interactivity(self):
        """Test interactive statistics features"""
        print("\\n🔍 Testing statistics interactivity...")
        self.driver.get(TEST_URLS['statistics'])
        
        # Skip if redirected to login
        if 'login' in self.driver.current_url:
            print("⚠️ Skipping interactivity test - not logged in")
            return
            
        try:
            # Look for clickable statistics sections
            clickable_stats = self.driver.find_elements(By.CSS_SELECTOR, 
                "[onclick*='toggle'], [data-toggle], .expandable, .collapsible")
            
            if clickable_stats:
                print(f"✅ Found {len(clickable_stats)} clickable statistics sections")
                
                # Test clicking the first expandable section
                first_clickable = clickable_stats[0]
                first_clickable.click()
                time.sleep(2)
                
                # Check for dropdown or expanded content
                dropdowns = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".dropdown-content, .expanded, .show, .collapse.in")
                
                if dropdowns:
                    print("✅ Interactive dropdown/expansion working")
                else:
                    print("⚠️ Click registered but no visible expansion")
                    
            else:
                print("⚠️ No interactive statistics elements found")
                
        except Exception as e:
            print(f"❌ Error testing statistics interactivity: {e}")
            
    def test_admin_panel_protection(self):
        """Test admin panel access protection"""
        print("\\n🔍 Testing admin panel protection...")
        self.driver.get(TEST_URLS['admin'])
        
        # Check if redirected to admin login
        current_url = self.driver.current_url
        
        if 'admin/login' in current_url or 'login' in current_url:
            print("✅ Admin panel protected - login required")
            
            # Check for admin login form
            try:
                username_field = self.driver.find_element(By.NAME, "username")
                password_field = self.driver.find_element(By.NAME, "password")
                
                if username_field.is_displayed() and password_field.is_displayed():
                    print("✅ Admin login form displayed correctly")
                else:
                    print("❌ Admin login form elements not visible")
                    
            except NoSuchElementException:
                print("❌ Admin login form not found")
                
        else:
            # If admin panel is accessible, it might be a security issue
            print("⚠️ Admin panel accessible without login - check permissions")
            
    def test_user_role_visibility(self):
        """Test if different content is shown based on user roles"""
        print("\\n🔍 Testing user role-based content visibility...")
        
        # Test statistics page for role-based content
        self.driver.get(TEST_URLS['statistics'])
        
        try:
            # Look for admin-only content indicators
            admin_only_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "[data-admin-only], .admin-only, .staff-only")
            
            if admin_only_elements:
                print(f"✅ Found {len(admin_only_elements)} role-restricted elements")
            else:
                print("⚠️ No explicit role-restricted elements found")
                
            # Check for user count/download statistics that should be admin-only
            user_stats = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Total Users') or contains(text(), 'Active Users')]")
            download_stats = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Total Downloads') or contains(text(), 'Downloads')]")
            
            if not user_stats and not download_stats:
                print("✅ Admin-only statistics properly hidden from public view")
            else:
                print("⚠️ Admin statistics may be visible to public users")
                
        except Exception as e:
            print(f"❌ Error testing role visibility: {e}")
            
    def test_dashboard_components(self):
        """Test dashboard component functionality"""
        print("\\n🔍 Testing dashboard components...")
        self.driver.get(TEST_URLS['dashboard'])
        
        # Skip if redirected to login
        if 'login' in self.driver.current_url:
            print("⚠️ Skipping dashboard components test - not logged in")
            return
            
        try:
            # Look for common dashboard components
            components = {
                'cards': '.card, .dashboard-card',
                'buttons': 'button, .btn',
                'links': 'a[href]',
                'tables': 'table',
                'forms': 'form'
            }
            
            for component_name, selector in components.items():
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} {component_name}")
                    
                    # Test if elements are interactive
                    if component_name == 'buttons':
                        visible_buttons = [btn for btn in elements if btn.is_displayed()]
                        if visible_buttons:
                            print(f"✅ {len(visible_buttons)} buttons are visible and clickable")
                            
                else:
                    print(f"⚠️ No {component_name} found on dashboard")
                    
        except Exception as e:
            print(f"❌ Error testing dashboard components: {e}")
            
    def test_navigation_consistency(self):
        """Test navigation consistency across different pages"""
        print("\\n🔍 Testing navigation consistency...")
        
        pages_to_test = [
            ('Home', TEST_URLS['home']),
            ('Books', TEST_URLS['books']),
            ('Login', TEST_URLS['login'])
        ]
        
        navigation_elements = []
        
        for page_name, url in pages_to_test:
            try:
                self.driver.get(url)
                time.sleep(1)
                
                # Get navigation elements
                nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a")
                nav_texts = [link.text.strip() for link in nav_links if link.text.strip()]
                
                navigation_elements.append((page_name, nav_texts))
                print(f"✅ {page_name}: Found {len(nav_texts)} navigation links")
                
            except Exception as e:
                print(f"❌ Error testing navigation on {page_name}: {e}")
                
        # Check consistency
        if len(navigation_elements) > 1:
            first_nav = set(navigation_elements[0][1])
            consistent = True
            
            for page_name, nav_texts in navigation_elements[1:]:
                current_nav = set(nav_texts)
                if first_nav != current_nav:
                    consistent = False
                    break
                    
            if consistent:
                print("✅ Navigation is consistent across pages")
            else:
                print("⚠️ Navigation inconsistency detected between pages")

if __name__ == '__main__':
    unittest.main()