import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# --- Test Steps ---
try:
    # 1. Open the URL with the CORRECT IP address.
    driver.get('http://127.0.0.1:8000/clubnest/signup/') # <<<<<<<<<<<<< FIXED HERE
    print("Successfully opened signup page.")
    time.sleep(1)

    # Generate a unique email using the current timestamp
    timestamp = int(time.time())
    unique_email = f"johndoe_{timestamp}@example.com"
    print(f"Generated unique email for this test: {unique_email}")

    # 2. Find and fill each form element.

    # First Name
    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'first_name')))
    first_name_field.send_keys('John')

    # Last Name
    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'last_name')))
    last_name_field.send_keys('Doe')
    print("Filled in first and last name.")

    # Department Dropdown
    department_select_element = wait.until(EC.presence_of_element_located((By.NAME, 'department')))
    department_select = Select(department_select_element)
    department_select.select_by_value('cse')
    print("Selected Department: CSE")

    # Semester Dropdown
    semester_select_element = wait.until(EC.presence_of_element_located((By.NAME, 'semester')))
    semester_select = Select(semester_select_element)
    semester_select.select_by_visible_text('3rd')
    print("Selected Semester: 3rd")

    # Email
    email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    email_field.send_keys(unique_email) # Use the unique email variable here
    print("Filled in email.")

    # Password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password1')))
    password_field.send_keys('MySecurePassword123')

    # Confirm Password
    confirm_password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password2')))
    confirm_password_field.send_keys('MySecurePassword123')
    print("Filled in password and confirmation.")
    time.sleep(1)

    # 3. Find the submit button and click it.
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    submit_button.click()
    print("Clicked the 'Sign Up' button.")

    # 4. Pause the script to see the result.
    print("Test completed. The browser will close in 10 seconds.")
    time.sleep(10)

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser closed.")