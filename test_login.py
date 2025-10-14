import time
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
    # --- FIXED LOGIN CREDENTIALS ---
    # Using the specific username and password you requested
    LOGIN_USERNAME = "sarna"
    LOGIN_PASSWORD = "123"
    # -------------------------------

    # Step 1: Open the login page from your running server
    # The URL has been updated to match your previous script
    driver.get('http://127.0.0.1:8000/clubnest/signin/')
    print("\nSuccessfully opened the login page.")

    # Step 2: Find the username field and enter "sarna"
    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(LOGIN_USERNAME)
    print(f"Entered username: '{LOGIN_USERNAME}'")
    time.sleep(0.5)

    # Step 3: Find the password field and enter "123"
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(LOGIN_PASSWORD)
    print(f"Entered password: '{LOGIN_PASSWORD}'")
    time.sleep(0.5)

    # Step 4: Find the "Sign In" button and click it
    signin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    signin_button.click()
    print("Clicked the 'Sign In' button.")

    # Step 5: Verify successful login by checking for redirection
    # A successful login usually redirects to a new page like '/home' or '/dashboard'.
    # Update '/home' if your application redirects to a different URL.
    print("Waiting for redirection after successful login...")
    wait.until(EC.url_contains("/home")) # Assuming successful login redirects to a URL containing "/home"
    print("✅ Login Successful! Redirected to the correct page.")

    # Step 6: Wait to observe the logged-in page
    print("\nTest finished. The browser will close in 7 seconds.")
    time.sleep(7)

except Exception as e:
    print(f"\n❌ An error occurred or login failed: {e}")
    print("Please check the following:")
    print("1. Is your Django server running?")
    print("2. Are the username 'sarna' and password '123' correct in your database?")
    print("3. Does the URL change to contain '/home' after a successful login?")

finally:
    # --- Teardown ---
    # Close the browser at the end of the test
    driver.quit()
    print("Browser has been closed.")