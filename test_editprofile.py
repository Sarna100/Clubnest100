import os
import time
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
wait = WebDriverWait(driver, 10)
print("WebDriver initialized.")

# --- Test Steps ---
try:
    # --- Configuration ---
    LOGIN_USERNAME = "sarna"
    LOGIN_PASSWORD = "123"
    SUCCESS_URL_PART = "/profile/"

    # --- Step 1: Login (Slowed Down) ---
    print("--- Step 1: Attempting to Log In (Slowly) ---")
    driver.get('http://127.0.0.1:8000/clubnest/signin/')

    # Type username slowly
    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(LOGIN_USERNAME)
    print("- Entered username.")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED

    # Type password slowly
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(LOGIN_PASSWORD)
    print("- Entered password.")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED

    # Click button
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    print("- Clicked Sign In.")

    # --- Step 2: VERIFY Login Success ---
    try:
        wait.until(EC.url_contains(SUCCESS_URL_PART))
        print(f"✅ Login Successful. Redirected to a URL containing '{SUCCESS_URL_PART}'.")
        time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED
    except TimeoutException:
        raise Exception("Login failed. Check credentials or the SUCCESS_URL_PART variable.")

    # --- Step 3: Navigate to Edit Profile Page ---
    print("\n--- Step 3: Navigating to Edit Profile Page ---")
    driver.get('http://127.0.0.1:8000/clubnest/profile/edit/')

    # --- Step 4: Update Form Fields (Slowed Down) ---
    print("Updating form fields slowly...")

    # Update First Name
    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'first_name')))
    first_name_field.clear()
    time.sleep(0.5)  # <<<<<<<<<<<<<<<< PAUSE ADDED
    first_name_field.send_keys("sarna")
    print("- Updated first name to 'sarna'.")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED

    # Update Last Name
    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'last_name')))
    last_name_field.clear()
    time.sleep(0.5)  # <<<<<<<<<<<<<<<< PAUSE ADDED
    last_name_field.send_keys("rani")
    print("- Updated last name to 'rani'.")
    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED

    # --- Step 5: Submit Form ---
    print("Finding the 'Save Changes' button...")
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Changes')]")))

    time.sleep(1)  # <<<<<<<<<<<<<<<< PAUSE ADDED before click
    driver.execute_script("arguments[0].click();", save_button)
    print("Clicked 'Save Changes' button using JavaScript.")

    # Increased the final wait time to 15 seconds
    print("\n✅ Test finished successfully. The browser will close in 15 seconds.")
    time.sleep(15)

except Exception as e:
    print(f"\n❌ An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser has been closed.")