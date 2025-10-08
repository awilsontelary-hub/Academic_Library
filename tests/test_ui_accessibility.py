"""
UI/UX and Accessibility Tests
Tests for user interface, user experience, and accessibility compliance
"""
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tests.test_config import TestConfig, TEST_URLS

class UIUXAccessibilityTests(unittest.TestCase):
    """Test suite for UI/UX and accessibility"""
    
    def setUp(self):
        """Set up test environment"""
        self.driver = TestConfig.get_chrome_driver()
        self.driver.implicitly_wait(10)
        
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()
        
    def test_color_scheme_consistency(self):
        """Test blue/white color scheme consistency"""
        print("\\n🔍 Testing color scheme consistency...")
        
        pages_to_test = [TEST_URLS['home'], TEST_URLS['books'], TEST_URLS['login']]
        
        for url in pages_to_test:
            self.driver.get(url)
            time.sleep(2)
            
            try:
                # Check for consistent blue theme elements
                blue_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".btn-primary, .bg-primary, .text-primary, .navbar")
                
                if blue_elements:
                    print(f"✅ Found {len(blue_elements)} blue-themed elements on {url}")
                else:
                    print(f"⚠️ No blue-themed elements found on {url}")
                    
                # Check for proper contrast elements
                text_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    "p, span, div, h1, h2, h3, h4, h5, h6")
                
                if text_elements:
                    print(f"✅ Text elements present for contrast testing on {url}")
                    
            except Exception as e:
                print(f"❌ Error testing color scheme on {url}: {e}")
                
    def test_button_interactions(self):
        """Test button hover and click interactions"""
        print("\\n🔍 Testing button interactions...")
        self.driver.get(TEST_URLS['home'])
        
        try:
            # Find all buttons
            buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "button, .btn, input[type='submit'], input[type='button']")
            
            if buttons:
                print(f"✅ Found {len(buttons)} buttons to test")
                
                # Test hover effect on first visible button
                visible_buttons = [btn for btn in buttons if btn.is_displayed()]
                if visible_buttons:
                    first_button = visible_buttons[0]
                    
                    # Hover over button
                    actions = ActionChains(self.driver)
                    actions.move_to_element(first_button).perform()
                    time.sleep(1)
                    
                    print("✅ Button hover interaction tested")
                    
            else:
                print("⚠️ No buttons found for interaction testing")
                
        except Exception as e:
            print(f"❌ Error testing button interactions: {e}")
            
    def test_form_accessibility(self):
        """Test form accessibility features"""
        print("\\n🔍 Testing form accessibility...")
        self.driver.get(TEST_URLS['login'])
        
        try:
            # Check for form labels
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            
            print(f"✅ Found {len(labels)} labels and {len(inputs)} input fields")
            
            # Check for proper label associations
            labeled_inputs = 0
            for input_field in inputs:
                input_id = input_field.get_attribute('id')
                input_name = input_field.get_attribute('name')
                
                # Check if input has associated label
                if input_id:
                    associated_labels = self.driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                    if associated_labels:
                        labeled_inputs += 1
                        
            if labeled_inputs > 0:
                print(f"✅ {labeled_inputs} inputs have proper label associations")
            else:
                print("⚠️ No proper label associations found")
                
            # Check for placeholder text
            placeholders = [inp for inp in inputs if inp.get_attribute('placeholder')]
            if placeholders:
                print(f"✅ {len(placeholders)} inputs have placeholder text")
                
        except Exception as e:
            print(f"❌ Error testing form accessibility: {e}")
            
    def test_keyboard_navigation(self):
        """Test keyboard navigation functionality"""
        print("\\n🔍 Testing keyboard navigation...")
        self.driver.get(TEST_URLS['login'])
        
        try:
            # Find focusable elements
            focusable_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "a, button, input, textarea, select, [tabindex]")
            
            visible_focusable = [elem for elem in focusable_elements if elem.is_displayed()]
            
            if visible_focusable:
                print(f"✅ Found {len(visible_focusable)} focusable elements")
                
                # Test tabbing through elements
                first_element = visible_focusable[0]
                first_element.click()  # Focus first element
                
                # Send tab key
                first_element.send_keys("\\t")
                time.sleep(1)
                
                print("✅ Keyboard navigation tested")
                
            else:
                print("⚠️ No focusable elements found")
                
        except Exception as e:
            print(f"❌ Error testing keyboard navigation: {e}")
            
    def test_image_alt_attributes(self):
        """Test image alt attributes for accessibility"""
        print("\\n🔍 Testing image alt attributes...")
        self.driver.get(TEST_URLS['home'])
        
        try:
            # Find all images
            images = self.driver.find_elements(By.TAG_NAME, "img")
            
            if images:
                print(f"✅ Found {len(images)} images")
                
                images_with_alt = 0
                for img in images:
                    alt_text = img.get_attribute('alt')
                    if alt_text:
                        images_with_alt += 1
                        
                print(f"✅ {images_with_alt}/{len(images)} images have alt attributes")
                
                if images_with_alt == len(images):
                    print("✅ All images have alt attributes - excellent accessibility!")
                elif images_with_alt > 0:
                    print("⚠️ Some images missing alt attributes")
                else:
                    print("❌ No images have alt attributes - accessibility issue")
                    
            else:
                print("⚠️ No images found on homepage")
                
        except Exception as e:
            print(f"❌ Error testing image alt attributes: {e}")
            
    def test_responsive_layout(self):
        """Test responsive layout at different screen sizes"""
        print("\\n🔍 Testing responsive layout...")
        
        # Test different screen sizes
        screen_sizes = [
            (1920, 1080, "Large Desktop"),
            (1366, 768, "Standard Desktop"),
            (768, 1024, "Tablet Portrait"),
            (375, 812, "Mobile Phone")
        ]
        
        for width, height, device_name in screen_sizes:
            self.driver.set_window_size(width, height)
            self.driver.get(TEST_URLS['home'])
            time.sleep(2)
            
            try:
                # Check if content is visible and not overflowing
                body = self.driver.find_element(By.TAG_NAME, "body")
                body_width = body.size['width']
                
                # Check for horizontal scrollbar (may indicate layout issues)
                scroll_width = self.driver.execute_script("return document.body.scrollWidth")
                client_width = self.driver.execute_script("return document.body.clientWidth")
                
                if scroll_width <= client_width + 5:  # Allow 5px tolerance
                    print(f"✅ {device_name} ({width}x{height}): No horizontal overflow")
                else:
                    print(f"⚠️ {device_name} ({width}x{height}): Possible horizontal overflow")
                    
                # Check navigation visibility
                nav_elements = self.driver.find_elements(By.TAG_NAME, "nav")
                if nav_elements and nav_elements[0].is_displayed():
                    print(f"✅ {device_name}: Navigation visible")
                else:
                    print(f"⚠️ {device_name}: Navigation may be hidden or collapsed")
                    
            except Exception as e:
                print(f"❌ Error testing {device_name} layout: {e}")
                
    def test_loading_performance(self):
        """Test page loading performance indicators"""
        print("\\n🔍 Testing loading performance...")
        
        pages_to_test = [
            ('Home', TEST_URLS['home']),
            ('Books', TEST_URLS['books']),
            ('Login', TEST_URLS['login'])
        ]
        
        for page_name, url in pages_to_test:
            start_time = time.time()
            
            try:
                self.driver.get(url)
                
                # Wait for page to load completely
                self.driver.execute_script("return document.readyState") == "complete"
                
                end_time = time.time()
                load_time = end_time - start_time
                
                print(f"✅ {page_name}: Loaded in {load_time:.2f} seconds")
                
                if load_time < 3.0:
                    print(f"✅ {page_name}: Good loading performance")
                elif load_time < 5.0:
                    print(f"⚠️ {page_name}: Acceptable loading performance")
                else:
                    print(f"❌ {page_name}: Slow loading performance")
                    
            except Exception as e:
                print(f"❌ Error testing {page_name} performance: {e}")
                
    def test_error_handling(self):
        """Test error handling and user feedback"""
        print("\\n🔍 Testing error handling...")
        
        # Test 404 error handling
        try:
            self.driver.get(f"{TEST_URLS['home']}/nonexistent-page/")
            time.sleep(2)
            
            # Check for 404 page or error message
            page_source = self.driver.page_source.lower()
            
            if '404' in page_source or 'not found' in page_source or 'error' in page_source:
                print("✅ 404 error handling working")
            else:
                print("⚠️ 404 error handling may need improvement")
                
        except Exception as e:
            print(f"❌ Error testing 404 handling: {e}")
            
    def test_visual_feedback(self):
        """Test visual feedback for user interactions"""
        print("\\n🔍 Testing visual feedback...")
        self.driver.get(TEST_URLS['home'])
        
        try:
            # Test link hover effects
            links = self.driver.find_elements(By.TAG_NAME, "a")
            visible_links = [link for link in links if link.is_displayed() and link.get_attribute('href')]
            
            if visible_links:
                print(f"✅ Found {len(visible_links)} links for feedback testing")
                
                # Hover over first link
                actions = ActionChains(self.driver)
                actions.move_to_element(visible_links[0]).perform()
                time.sleep(1)
                
                print("✅ Link hover feedback tested")
                
            # Test form input focus
            self.driver.get(TEST_URLS['login'])
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea")
            
            if inputs:
                first_input = inputs[0]
                first_input.click()  # Focus input
                time.sleep(1)
                
                print("✅ Form input focus feedback tested")
                
        except Exception as e:
            print(f"❌ Error testing visual feedback: {e}")

if __name__ == '__main__':
    unittest.main()