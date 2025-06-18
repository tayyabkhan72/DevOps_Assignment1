# tests/test_login.py
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

def test_login_with_correct_credentials(driver):
    """
    Test Case: Login with correct credentials.
    Verifies that a pre-existing user can log in and is redirected to the home page.
    """
    print("\n--- Starting Test: Login With Correct Credentials ---")

    print("Navigating to /login page...")
    driver.get("http://web/login")
    
    wait = WebDriverWait(driver, 10)

    print("Finding and filling out the login form with correct credentials...")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("tayyab.khan72")
    driver.find_element(By.NAME, "password").send_keys("tayyab47khan")
    
    print("Clicking the 'Login' button...")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    print("Asserting redirection to the /home page...")
    wait.until(EC.url_contains("/home"))
    assert "/home" in driver.current_url

    print("--- Test Passed: Login With Correct Credentials ---")


def test_login_with_wrong_credentials(driver):
    """
    Test Case: Login with wrong credentials.
    Verifies that using an incorrect password fails and shows an alert.
    """
    print("\n--- Starting Test: Login With Wrong Credentials ---")

    print("Navigating to /login page...")
    driver.get("http://web/login")
    
    wait = WebDriverWait(driver, 10)

    print("Finding and filling out the login form with wrong credentials...")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpassword")
    
    print("Clicking the 'Login' button...")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    print("Asserting that an alert with 'Wrong Credentials' appears...")
    alert = wait.until(EC.alert_is_present())
    assert "Wrong Credentials" in alert.text
    alert.accept()

    print("Asserting that the page URL is still /login...")
    assert "/login" in driver.current_url

    print("--- Test Passed: Login With Wrong Credentials ---")


def test_login_with_empty_fields(driver):
    """
    Test Case: Login with empty fields.
    Verifies that submitting an empty form fails and shows an alert.
    """
    print("\n--- Starting Test: Login With Empty Fields ---")

    print("Navigating to /login page...")
    driver.get("http://web/login")

    wait = WebDriverWait(driver, 10)

    print("Clicking 'Login' button with empty fields...")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    print("Asserting that an alert appears...")
    alert = wait.until(EC.alert_is_present())
    alert.accept()

    print("Asserting that the page URL is still /login...")
    assert "/login" in driver.current_url

    print("--- Test Passed: Login With Empty Fields ---")