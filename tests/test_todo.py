# tests/test_todo.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def perform_login(driver, wait):
    print("...Logging in to access home page...")
    driver.get("http://web/login")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    try:
        alert = wait.until(EC.alert_is_present())
        assert "Login Successful" in alert.text
        alert.accept()
    except:
        print("...Warning: Could not handle login alert.")

    wait.until(EC.url_contains("/home"))
    print("...Login successful and redirected to home...")

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_add_task(driver):
    print("\n--- Starting Test: Add a Task ---")
    wait = WebDriverWait(driver, 20)
    perform_login(driver, wait)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    task_name = f"My new automated task {int(time.time())}"
    print(f"Adding task: '{task_name}'")
    
    task_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".create_form input")))
    task_input.send_keys(task_name)
    driver.find_element(By.CSS_SELECTOR, ".create_form button").click()
    
    task_xpath = f"//p[contains(text(), '{task_name}')]"
    new_task_element = wait.until(EC.visibility_of_element_located((By.XPATH, task_xpath)))
    assert new_task_element.is_displayed()
    
    print("--- Test Passed: Add a Task ---")

def test_delete_task(driver):
    print("\n--- Starting Test: Delete a Task ---")
    wait = WebDriverWait(driver, 20)
    perform_login(driver, wait)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    task_to_delete = f"Task to be deleted {int(time.time())}"
    print(f"Setup: Creating a task to delete: '{task_to_delete}'")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".create_form input"))).send_keys(task_to_delete)
    driver.find_element(By.CSS_SELECTOR, ".create_form button").click()

    task_xpath = f"//p[contains(text(), '{task_to_delete}')]"
    wait.until(EC.visibility_of_element_located((By.XPATH, task_xpath)))
    print("Setup complete. Task created.")
    
    # The fix: Wait for the specific delete icon to be clickable
    task_div_xpath = f"//p[contains(text(), '{task_to_delete}')]/ancestor::div[@class='task']"
    task_div = wait.until(EC.presence_of_element_located((By.XPATH, task_div_xpath)))
    delete_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span .bs-fill-trash-fill")))
    
    print("Clicking the delete icon...")
    delete_icon.click()

    print("Asserting that the task is no longer in the list...")
    is_gone = wait.until(EC.invisibility_of_element_located((By.XPATH, task_xpath)))
    assert is_gone
    
    print("--- Test Passed: Delete a Task ---")