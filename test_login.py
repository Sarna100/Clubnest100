import time
import random
import string  # Required to generate random strings for the password
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
# Automatically sets up and launches the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Creates a waiter object that will wait up to 10 seconds for an element
wait = WebDriverWait(driver, 10)
print("WebDriver initialized.")

# --- Test Steps ---
try:
    # Step 1: Generate random credentials for the test
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    random_email = f"test_{random_part}@example.com"

    password_chars = string.ascii_letters + string.digits
    random_password = ''.join(random.choices(password_chars, k=12))

    print("--- Random Credentials Generated for This Test ---")
    print(f"Email: {random_email}")
    print(f"Password: {random_password}")
    print("-------------------------------------------------")

    # Step 2: Open the login page from your running server
    # Make sure your Django server is running before you execute this.
    driver.get('http://127.0.0.1:8000/clubnest/signin/')  # Change this URL if yours is different
    print("\nSuccessfully opened the login page.")

    # Step 3: Find the username field and enter the random email
    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(random_email)
    print("Entered the random email.")
    time.sleep(0.5)

    # Step 4: Find the password field and enter the random password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(random_password)
    print("Entered the random password.")
    time.sleep(0.5)

    # Step 5: Find the "Sign In" button and click it
    signin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    signin_button.click()
    print("Clicked the 'Sign In' button.")

    # Step 6: Wait to observe the result
    # Since the credentials are random, the login should fail, which proves the form submission works.
    print("\nTest finished. The browser will close in 7 seconds.")
    time.sleep(7)

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print(
        "IMPORTANT: Please make sure your Django server is running and the login page is available at http://127.0.0.1:8000/signin/")

finally:
    # --- Teardown ---
    # Close the browser at the end of the test
    driver.quit()
    print("Browser has been closed.")