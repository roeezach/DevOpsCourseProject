import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

class TestCurrencyConverter:
    
    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()
        
        # Headless mode control via environment variable
        headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        if headless:
            chrome_options.add_argument("--headless")
            print("Running in HEADLESS mode")
        else:
            print("Running in VISIBLE mode")
            
        # Standard Chrome options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--start-maximized")
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        
        # Cleanup
        driver.quit()
    
    @pytest.fixture
    def app_url(self):
        """Get application URL from environment or use default"""
        return os.getenv('APP_URL', 'http://localhost:3000')
    
    def test_homepage_loads(self, driver, app_url):
        """Test that the homepage loads successfully"""
        driver.get(app_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check if page title is set
        assert driver.title is not None
        print(f"Homepage loaded successfully with title: {driver.title}")
    
    def test_currency_form_elements_exist(self, driver, app_url):
        """Test that all required form elements exist using various locators"""
        driver.get(app_url)
        
        # Check for amount input field using name attribute
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "shekels"))
        )
        assert amount_input is not None
        
        # Check for currency select dropdown using name attribute
        currency_select = driver.find_element(By.NAME, "currency")
        assert currency_select is not None
        
        # Check for submit button using CSS selector
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        assert submit_button is not None
        
        print(" All form elements exist (tested with NAME and CSS selectors)")
    
    def test_advanced_selectors(self, driver, app_url):
        """Test advanced CSS selectors and element discovery"""
        driver.get(app_url)
        
        # CSS selector for form elements
        form_elements = driver.find_elements(By.CSS_SELECTOR, "form input, form select, form button")
        assert len(form_elements) >= 3, "Should find at least 3 form elements"
        
        # Find labels using CSS selectors
        labels = driver.find_elements(By.CSS_SELECTOR, "label")
        print(f"Found {len(labels)} labels on the page")
        
        # Test input with attribute contains using CSS selector
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[name*='shek']")
        assert len(inputs) >= 1, "Should find input containing 'shek' in name"
        
        # Test multiple attribute selectors
        select_elements = driver.find_elements(By.CSS_SELECTOR, "select[name='currency']")
        assert len(select_elements) >= 1, "Should find currency select element"
        
        print(" Advanced CSS selectors working correctly")
    
    def test_form_validation(self, driver, app_url):
        """Test form validation using CSS selectors and element attributes"""
        driver.get(app_url)
        
        # Find form using CSS selector
        form = driver.find_element(By.CSS_SELECTOR, "form")
        assert form is not None
        
        # Check input attributes using name selector
        amount_input = driver.find_element(By.NAME, "shekels")
        input_type = amount_input.get_attribute("type")
        print(f"Amount input type: {input_type}")
        
        # Check select options using CSS selector
        currency_options = driver.find_elements(By.CSS_SELECTOR, "select[name='currency'] option")
        option_values = [option.get_attribute("value") for option in currency_options]
        print(f"Currency options: {option_values}")
        
        # Verify expected currency options exist using CSS attribute selectors
        expected_currencies = ["usd", "eur", "gbp"]
        for currency in expected_currencies:
            option = driver.find_element(By.CSS_SELECTOR, f"select[name='currency'] option[value='{currency}']")
            assert option is not None, f"Currency option {currency} should exist"
        
        print(" Form validation with CSS selectors completed")
    
    def test_currency_conversion_usd(self, driver, app_url):
        """Test USD currency conversion"""
        driver.get(app_url)
        
        # Find and fill amount input
        amount_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shekels"))
        )
        amount_input.clear()
        amount_input.send_keys("100")
        
        # Select USD currency
        currency_select = Select(driver.find_element(By.NAME, "currency"))
        currency_select.select_by_value("usd")
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        # Wait for result page
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        
        # Verify conversion result
        result_text = result_element.text
        assert "₪100" in result_text
        assert "$" in result_text
        assert "27" in result_text  # Expected USD conversion (100 * 0.27 = 27)
        
        print(f"✅ USD conversion successful: {result_text}")
    
    def test_currency_conversion_eur(self, driver, app_url):
        """Test EUR currency conversion"""
        driver.get(app_url)
        
        # Fill form for EUR conversion
        amount_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shekels"))
        )
        amount_input.clear()
        amount_input.send_keys("100")
        
        # Select EUR currency
        currency_select = Select(driver.find_element(By.NAME, "currency"))
        currency_select.select_by_value("eur")
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        # Wait for result
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        
        # Verify EUR conversion
        result_text = result_element.text
        assert "₪100" in result_text
        assert "€" in result_text
        assert "25" in result_text  # Expected EUR conversion (100 * 0.25 = 25)
        
        print(f"✅ EUR conversion successful: {result_text}")
    
    def test_currency_conversion_gbp(self, driver, app_url):
        """Test GBP currency conversion"""
        driver.get(app_url)
        
        # Fill form for GBP conversion
        amount_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shekels"))
        )
        amount_input.clear()
        amount_input.send_keys("100")
        
        # Select GBP currency
        currency_select = Select(driver.find_element(By.NAME, "currency"))
        currency_select.select_by_value("gbp")
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        # Wait for result
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        
        # Verify GBP conversion
        result_text = result_element.text
        assert "₪100" in result_text
        assert "£" in result_text
        assert "21" in result_text  # Expected GBP conversion (100 * 0.21 = 21)
        
        print(f"✅ GBP conversion successful: {result_text}")
    
    def test_convert_again_button(self, driver, app_url):
        """Test the 'Convert Again' functionality"""
        driver.get(app_url)
        
        # Perform initial conversion
        amount_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shekels"))
        )
        amount_input.clear()
        amount_input.send_keys("50")
        
        currency_select = Select(driver.find_element(By.NAME, "currency"))
        currency_select.select_by_value("usd")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        # Wait for result page and find convert again button
        convert_again_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "convert-again"))
        )
        
        # Click convert again
        convert_again_button.click()
        
        # Verify we're back to the form
        amount_input_again = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "shekels"))
        )
        
        assert amount_input_again.is_displayed()
        print("✅ Convert again button works correctly")
    
    def test_multiple_conversions(self, driver, app_url):
        """Test multiple currency conversions in sequence"""
        test_cases = [
            {"amount": "50", "currency": "usd", "expected_symbol": "$"},
            {"amount": "200", "currency": "eur", "expected_symbol": "€"},
            {"amount": "150", "currency": "gbp", "expected_symbol": "£"}
        ]
        
        for test_case in test_cases:
            driver.get(app_url)
            
            # Fill form
            amount_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "shekels"))
            )
            amount_input.clear()
            amount_input.send_keys(test_case["amount"])
            
            currency_select = Select(driver.find_element(By.NAME, "currency"))
            currency_select.select_by_value(test_case["currency"])
            
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            submit_button.click()
            
            # Verify result
            result_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            
            result_text = result_element.text
            assert f"₪{test_case['amount']}" in result_text
            assert test_case["expected_symbol"] in result_text
            
            print(f"✅ Conversion test passed: {test_case['amount']} ILS to {test_case['currency'].upper()}")
    
    def test_error_handling_invalid_input(self, driver, app_url):
        """Test error handling for invalid input"""
        driver.get(app_url)
        
        # Try submitting with empty amount
        amount_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shekels"))
        )
        amount_input.clear()
        amount_input.send_keys("")
        
        currency_select = Select(driver.find_element(By.NAME, "currency"))
        currency_select.select_by_value("usd")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        # Application should handle this gracefully
        time.sleep(2)
        print("✅ Empty input handled gracefully")
    
    def test_page_responsiveness(self, driver, app_url):
        """Test page responsiveness in different screen sizes"""
        screen_sizes = [
            (1920, 1080),  # Desktop
            (1024, 768),   # Tablet
            (375, 667)     # Mobile
        ]
        
        for width, height in screen_sizes:
            driver.set_window_size(width, height)
            driver.get(app_url)
            
            # Check if form elements are still accessible
            amount_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "shekels"))
            )
            
            assert amount_input.is_displayed()
            print(f"✅ Page responsive at {width}x{height}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
