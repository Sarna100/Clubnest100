import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

# --- Setup ---
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)
print("WebDriver initialized.")

# --- Test Steps ---
try:
    # --- Configuration ---
    LOGIN_USERNAME = "sarna"
    LOGIN_PASSWORD = "123"
    SUCCESS_URL_PART = "/profile/"

    # --- Step 1: Login ---
    print("--- Step 1: Attempting to Log In ---")
    driver.get('http://127.0.0.1:8000/clubnest/signin/')
    wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(LOGIN_USERNAME)
    wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(LOGIN_PASSWORD)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

    # --- Step 2: VERIFY Login Success ---
    try:
        wait.until(EC.url_contains(SUCCESS_URL_PART))
        print(f"✅ Login Successful. Redirected to a URL containing '{SUCCESS_URL_PART}'.")
    except TimeoutException:
        raise Exception("Login failed. Check credentials or the SUCCESS_URL_PART variable.")

    # --- Step 3: Navigate to Edit Profile Page ---
    print("\n--- Step 3: Navigating to Edit Profile Page ---")
    driver.get('http://127.0.0.1:8000/clubnest/profile/edit/')

    # --- Step 4: Generate and Fill Form with RANDOM Data (Slowly) ---
    print("Updating form fields with random data...")

    # A) Generate and input random First and Last Name
    first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Jamie", "Riley"]
    last_names = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson"]
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)

    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'first_name')))
    first_name_field.clear()
    time.sleep(0.5)  # <<<<<<<<<<<<<<<< PAUSE
    first_name_field.send_keys(random_first_name)
    print(f"- Updated first name to: '{random_first_name}'")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE

    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'last_name')))
    last_name_field.clear()
    time.sleep(0.5)  # <<<<<<<<<<<<<<<< PAUSE
    last_name_field.send_keys(random_last_name)
    print(f"- Updated last name to: '{random_last_name}'")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE

    # B) Generate and input a unique random Email
    random_part = ''.join(random.choices(string.digits, k=5))
    random_email = f"{random_first_name.lower()}.{random_last_name.lower()}{random_part}@example.com"
    email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    email_field.clear()
    time.sleep(0.5)  # <<<<<<<<<<<<<<<< PAUSE
    email_field.send_keys(random_email)
    print(f"- Updated email to: '{random_email}'")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE

    # C) Randomly select a Department
    department_element = wait.until(EC.element_to_be_clickable((By.NAME, 'department')))
    department_dropdown = Select(department_element)
    all_dept_options = department_dropdown.options[1:]
    random_dept_option = random.choice(all_dept_options)
    department_dropdown.select_by_visible_text(random_dept_option.text)
    print(f"- Randomly selected department: '{random_dept_option.text}'")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE

    # D) Randomly select a Semester
    semester_element = wait.until(EC.element_to_be_clickable((By.NAME, 'semester')))
    semester_dropdown = Select(semester_element)
    all_sem_options = semester_dropdown.options[1:]
    random_sem_option = random.choice(all_sem_options)
    semester_dropdown.select_by_visible_text(random_sem_option.text)
    print(f"- Randomly selected semester: '{random_sem_option.text}'")
    time.sleep(2)  # A final pause to see all the random data entered

    # --- Step 5: Submit Form ---
    print("Finding the 'Save Changes' button...")
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Changes')]")))
    driver.execute_script("arguments[0].click();", save_button)
    print("Clicked 'Save Changes' button.")

    print("\n✅ Test finished successfully. The browser will close in 15 seconds.")
    time.sleep(15)

except Exception as e:
    print(f"\n❌ An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser has been closed.")