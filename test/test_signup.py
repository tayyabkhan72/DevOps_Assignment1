# tests/test_signup.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_successful_registration(driver):
    """
    Test Case: Sign up correctly.
    Verifies that a new user with unique credentials can register successfully
    and is redirected to the login page.
    """
    print("\n--- Starting Test: Successful Registration ---")
    
    unique_email = f"testuser_{int(time.time())}@example.com"
    
    print("Navigating to /register page...")
    driver.get("http://web:8081/register")
    
    wait = WebDriverWait(driver, 10)

    print("Finding and filling out the registration form...")
    wait.until(EC.visibility_of_element_located((By.NAME, "name"))).send_keys("Test User")
    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "password").send_keys("password123")
    
    print("Clicking the 'Register' button...")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    print("Asserting redirection to the /login page...")
    wait.until(EC.url_contains("/login"))
    assert "/login" in driver.current_url
    
    print("--- Test Passed: Successful Registration ---")


def test_registration_with_empty_fields(driver):
    """
    Test Case: Sign up with empty fields.
    Verifies that clicking 'Register' with empty fields does not navigate away.
    """
    print("\n--- Starting Test: Registration With Empty Fields ---")

    print("Navigating to /register page...")
    driver.get("http://web:8081/register")

    wait = WebDriverWait(driver, 10)

    print("Finding and clicking the 'Register' button without filling fields...")
    register_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    register_button.click()

    # Allow a moment for a potential navigation to occur
    time.sleep(1) 

    print("Asserting that the page URL is still /register...")
    # The expected behavior is to remain on the registration page
    assert "/register" in driver.current_url

    print("--- Test Passed: Registration With Empty Fields ---")