import os
import time
import random  # <<<<<<<<<<<<<<<< IMPORT THE RANDOM LIBRARY
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
print("WebDriver initialized.")

# --- Test Steps ---
try:
    # 1. Open your Django server URL for the club list
    driver.get('http://127.0.0.1:8000/clubnest/clubs/')
    print(f"Successfully opened the club list page.")

    # --- TEST CASE 1: SEARCH FOR A CLUB ---
    print("\n--- Testing Search Functionality ---")

    # <<<<<<<<<<<<<<<< NEW CODE STARTS HERE >>>>>>>>>>>>>>>>
    # Create a list of possible search terms
    search_options = ["Tech", "Art", "Sports", "Music", "Science", "Robotics"]
    # Choose a random item from the list
    random_search_query = random.choice(search_options)
    # <<<<<<<<<<<<<<<< NEW CODE ENDS HERE >>>>>>>>>>>>>>>>

    # 2. Find the search input field and type the random search query
    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))

    # <<<<<<<<<<<<<<<< UPDATED THIS LINE >>>>>>>>>>>>>>>>
    search_box.send_keys(random_search_query)
    print(f"Randomly selected and typed '{random_search_query}' into the search box.")
    # <<<<<<<<<<<<<<<< END OF UPDATE >>>>>>>>>>>>>>>>>>>>
    time.sleep(1)

    # 3. Find the search button and click it
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form button[type="submit"]')))
    search_button.click()
    print("Clicked the search button.")
    time.sleep(2)

    # --- TEST CASE 2: CLICK A "JOIN" BUTTON ---
    print("\n--- Testing 'Join Club' Button ---")

    # Go back to the main clubs page to reset the search for the next part of the test
    driver.get('http://127.0.0.1:8000/clubnest/clubs/')
    print("Navigated back to the main club list to test the join button.")

    # 4. Find the first available "Join Club" button and click it
    join_buttons = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Join Club')]")))

    if join_buttons:
        first_join_button = join_buttons[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", first_join_button)
        time.sleep(1)
        first_join_button.click()
        print("Successfully clicked the first available 'Join Club' button.")
    else:
        print("INFO: No 'Join Club' buttons were found on the page.")

    # 5. Wait to observe the final result
    print("\nTest completed. The browser will close in 7 seconds.")
    time.sleep(7)

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser has been closed.")