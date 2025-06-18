# tests/test_todo.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Helper function to perform login, to avoid repeating code
def perform_login(driver, wait):
    """
    Helper function to log into the application.
    It now correctly handles the success alert after logging in.
    """
    print("...Logging in to access home page...")
    driver.get("http://web/login")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("tayyab.khan72")
    driver.find_element(By.NAME, "password").send_keys("tayyab47khan")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # --- CORRECTED SECTION ---
    # We must handle the "Login Successful" alert to allow navigation to continue.
    print("...Accepting login success alert...")
    try:
        alert = wait.until(EC.alert_is_present())
        assert "Login Successful" in alert.text
        alert.accept()
    except Exception as e:
        print(f"...Warning: Could not handle login alert. Continuing... Error: {e}")

    # Now we wait for the redirection to the home page
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
    """
    Test Case: Add a task to the to-do list.
    Logs in, adds a new task, and verifies it appears in the list.
    """
    print("\n--- Starting Test: Add a Task ---")
    wait = WebDriverWait(driver, 20)
    perform_login(driver, wait)

    task_name = f"My new automated task {int(time.time())}"
    print(f"Adding task: '{task_name}'")
    
    task_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".create_form input")))
    task_input.send_keys(task_name)
    driver.find_element(By.CSS_SELECTOR, ".create_form button").click()
    
    print("Asserting that the new task is visible in the list...")
    # The page reloads, so we wait for an element with our unique task text to appear
    task_xpath = f"//p[contains(text(), '{task_name}')]"
    new_task_element = wait.until(EC.visibility_of_element_located((By.XPATH, task_xpath)))
    assert new_task_element.is_displayed()
    
    print("--- Test Passed: Add a Task ---")


def test_delete_task(driver):
    """
    Test Case: Delete a task from the to-do list.
    Logs in, adds a new task to ensure one exists, and then deletes it.
    """
    print("\n--- Starting Test: Delete a Task ---")
    wait = WebDriverWait(driver, 20)
    perform_login(driver, wait)

    # SETUP: First, create a task so we have something to delete
    task_to_delete = f"Task to be deleted {int(time.time())}"
    print(f"Setup: Creating a task to delete: '{task_to_delete}'")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".create_form input"))).send_keys(task_to_delete)
    driver.find_element(By.CSS_SELECTOR, ".create_form button").click()

    # Wait for the task to appear after reload
    task_xpath = f"//p[contains(text(), '{task_to_delete}')]"
    wait.until(EC.visibility_of_element_located((By.XPATH, task_xpath)))
    print("Setup complete. Task created.")
    

    # ACTION: Now, delete the task
    print("Finding the delete icon for the new task...")
    task_div_xpath = f"//p[contains(text(), '{task_to_delete}')]/ancestor::div[@class='task']"
    task_div = driver.find_element(By.XPATH, task_div_xpath)
    delete_icon = task_div.find_element(By.CSS_SELECTOR, ".icon.bs-fill-trash-fill")
    
    print("Clicking the delete icon...")
    delete_icon.click()

    # ASSERTION: Verify the task is no longer visible
    print("Asserting that the task is no longer in the list...")
    is_gone = wait.until(EC.invisibility_of_element_located((By.XPATH, task_xpath)))
    assert is_gone
    
    print("--- Test Passed: Delete a Task ---")