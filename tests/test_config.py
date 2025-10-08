"""
Selenium Test Configuration
Sets up the test environment for automated browser testing
"""
import os
import django
from django.conf import settings
from django.test.utils import get_runner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Django settings for testing
if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'online_library.settings'
    django.setup()

class TestConfig:
    """Base configuration for Selenium tests"""
    
    @staticmethod
    def get_chrome_driver():
        """Get Chrome WebDriver with optimal settings"""
        chrome_options = Options()
        
        # Add Chrome options for better testing
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # For headless testing (uncomment if needed)
        # chrome_options.add_argument('--headless')
        
        # Set up Chrome service with webdriver-manager
        service = Service(ChromeDriverManager().install())
        
        return webdriver.Chrome(service=service, options=chrome_options)
    
    @staticmethod
    def wait_for_element(driver, by, value, timeout=10):
        """Wait for element to be present"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    @staticmethod
    def wait_for_clickable(driver, by, value, timeout=10):
        """Wait for element to be clickable"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

# Test URLs
BASE_URL = 'http://127.0.0.1:8000'
TEST_URLS = {
    'home': f'{BASE_URL}/',
    'login': f'{BASE_URL}/accounts/login/',
    'register': f'{BASE_URL}/accounts/register/',
    'books': f'{BASE_URL}/books/',
    'statistics': f'{BASE_URL}/statistics/',
    'admin': f'{BASE_URL}/admin/',
    'dashboard': f'{BASE_URL}/dashboard/',
}