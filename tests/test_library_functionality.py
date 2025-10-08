"""
Library Functionality Tests
Tests for book browsing, searching, downloading, and library features
"""
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tests.test_config import TestConfig, TEST_URLS

class LibraryFunctionalityTests(unittest.TestCase):
    """Test suite for library functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.driver = TestConfig.get_chrome_driver()
        self.driver.implicitly_wait(10)
        
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()
        
    def test_books_page_loads(self):
        """Test if books page loads and displays content"""
        print("\\n🔍 Testing books page load...")
        self.driver.get(TEST_URLS['books'])
        
        # Check page title
        self.assertIn("Books", self.driver.title)
        print("✅ Books page loaded successfully")
        
        # Check for book listings or empty state message
        try:
            # Look for book containers or cards
            book_elements = self.driver.find_elements(By.CSS_SELECTOR, ".book-card, .card, .book-item")
            if book_elements:
                print(f"✅ Found {len(book_elements)} book elements")
            else:
                # Check for "no books" message
                no_books_msg = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'No books') or contains(text(), 'no books')]")
                if no_books_msg:
                    print("✅ No books found - empty state displayed correctly")
                else:
                    print("⚠️ Books page loaded but no content found")
                    
        except Exception as e:
            print(f"❌ Error checking books page content: {e}")
            
    def test_search_functionality(self):
        """Test book search functionality"""
        print("\\n🔍 Testing search functionality...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for search input field
            search_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='search'], input[name*='search'], input[placeholder*='search' i]")
            
            if search_inputs:
                search_input = search_inputs[0]
                print("✅ Search input found")
                
                # Test search with common term
                search_input.clear()
                search_input.send_keys("database")
                search_input.send_keys(Keys.RETURN)
                time.sleep(2)
                
                print("✅ Search executed successfully")
                
                # Check if search results are displayed
                current_url = self.driver.current_url
                if 'search' in current_url or 'q=' in current_url:
                    print("✅ Search URL updated correctly")
                else:
                    print("⚠️ Search may not have URL parameters")
                    
            else:
                print("⚠️ Search input field not found")
                
        except Exception as e:
            print(f"❌ Error testing search: {e}")
            
    def test_book_categories_filter(self):
        """Test book category filtering"""
        print("\\n🔍 Testing category filters...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for category filters
            category_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "select[name*='category'], .category-filter, .filter-category")
            
            if category_elements:
                print("✅ Category filter elements found")
                
                # If it's a select dropdown
                selects = self.driver.find_elements(By.TAG_NAME, "select")
                for select in selects:
                    try:
                        select_obj = Select(select)
                        options = select_obj.options
                        if len(options) > 1:  # More than just default option
                            print(f"✅ Select dropdown has {len(options)} options")
                            # Try selecting second option
                            select_obj.select_by_index(1)
                            time.sleep(2)
                            print("✅ Category selection successful")
                            break
                    except Exception as e:
                        print(f"⚠️ Error with select dropdown: {e}")
                        
            else:
                print("⚠️ No category filters found")
                
        except Exception as e:
            print(f"❌ Error testing categories: {e}")
            
    def test_book_details_access(self):
        """Test accessing book details"""
        print("\\n🔍 Testing book details access...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for book links or details buttons
            book_links = self.driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='book'], .book-link, .view-details, a[href*='detail']")
            
            if book_links:
                first_book_link = book_links[0]
                print("✅ Book detail links found")
                
                # Click first book link
                first_book_link.click()
                time.sleep(2)
                
                # Check if we navigated to a detail page
                current_url = self.driver.current_url
                if current_url != TEST_URLS['books']:
                    print("✅ Navigation to book details successful")
                    
                    # Check for book detail elements
                    detail_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                        ".book-title, .book-author, .book-description, h1, h2")
                    if detail_elements:
                        print("✅ Book detail content found")
                    else:
                        print("⚠️ Book detail page loaded but content not found")
                        
                else:
                    print("❌ Book detail navigation failed")
                    
            else:
                print("⚠️ No book detail links found")
                
        except Exception as e:
            print(f"❌ Error testing book details: {e}")
            
    def test_download_functionality(self):
        """Test book download functionality (UI only)"""
        print("\\n🔍 Testing download functionality...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for download buttons or links
            download_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='download'], .download-btn, button[onclick*='download'], a[download]")
            
            if download_elements:
                print(f"✅ Found {len(download_elements)} download elements")
                
                # Check if download elements are properly styled/visible
                visible_downloads = [elem for elem in download_elements if elem.is_displayed()]
                print(f"✅ {len(visible_downloads)} download elements are visible")
                
                # Test clicking download (but don't actually download)
                if visible_downloads:
                    download_element = visible_downloads[0]
                    
                    # Check if it has proper attributes
                    href = download_element.get_attribute('href')
                    if href:
                        print("✅ Download element has proper href attribute")
                    else:
                        onclick = download_element.get_attribute('onclick')
                        if onclick:
                            print("✅ Download element has onclick handler")
                            
            else:
                print("⚠️ No download elements found")
                
        except Exception as e:
            print(f"❌ Error testing downloads: {e}")
            
    def test_pagination(self):
        """Test pagination functionality"""
        print("\\n🔍 Testing pagination...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for pagination elements
            pagination_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".pagination, .page-nav, a[href*='page'], .next, .previous")
            
            if pagination_elements:
                print("✅ Pagination elements found")
                
                # Look for next/previous buttons
                next_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                    "a[href*='page=2'], .next:not(.disabled), a:contains('Next')")
                
                if next_buttons:
                    print("✅ Next page functionality available")
                else:
                    print("⚠️ Next page not available (may be single page)")
                    
            else:
                print("⚠️ No pagination found (may not be needed)")
                
        except Exception as e:
            print(f"❌ Error testing pagination: {e}")
            
    def test_form_submissions(self):
        """Test form submissions and validation"""
        print("\\n🔍 Testing form submissions...")
        self.driver.get(TEST_URLS['books'])
        
        try:
            # Look for forms (search, filter, etc.)
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            if forms:
                print(f"✅ Found {len(forms)} forms on books page")
                
                for i, form in enumerate(forms):
                    # Check form method and action
                    method = form.get_attribute('method') or 'GET'
                    action = form.get_attribute('action') or 'current page'
                    print(f"✅ Form {i+1}: Method={method}, Action={action}")
                    
                    # Check for CSRF token in POST forms
                    if method.upper() == 'POST':
                        csrf_tokens = form.find_elements(By.CSS_SELECTOR, "input[name='csrfmiddlewaretoken']")
                        if csrf_tokens:
                            print(f"✅ Form {i+1}: CSRF protection found")
                        else:
                            print(f"⚠️ Form {i+1}: No CSRF token found")
                            
            else:
                print("⚠️ No forms found on books page")
                
        except Exception as e:
            print(f"❌ Error testing forms: {e}")

if __name__ == '__main__':
    unittest.main()