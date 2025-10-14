import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
# Automatically configures and starts the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Sets up a waiter that will wait up to 10 seconds for elements to appear
wait = WebDriverWait(driver, 10)
print("WebDriver initialized successfully.")

# --- Test Steps ---
try:
    # 1. Open your local sponsor_list.html file
    file_path = os.path.abspath('sponsor_list.html')
    driver.get(f'http://127.0.0.1:8000/clubnest/sponsors/')
    print(f"Successfully opened the file: {file_path}")

    # 2. Find the "Contact us" link in the footer and click it
    # We use `By.LINK_TEXT` to find an <a> tag by its visible text.
    # We also use an explicit wait to ensure the page is loaded before we search.
    print("Searching for the 'Contact us' link in the footer...")
    contact_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Contact us')))

    # Optional: Scroll the element into view to ensure it is clickable
    driver.execute_script("arguments[0].scrollIntoView(true);", contact_link)
    time.sleep(0.5)  # A small pause after scrolling

    contact_link.click()
    print("Successfully clicked the 'Contact us' link.")

    # 3. Wait to observe the result
    # In a real test, you would check if the click led to a new page or a contact form.
    # For this demonstration, we'll just pause.
    print("Test completed. The browser will close in 5 seconds.")
    time.sleep(0.5)

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    # 4. Close the browser window to end the session
    driver.quit()
    print("Browser has been closed.")