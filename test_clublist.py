import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
LOGIN_URL = 'http://127.0.0.1:8000/clubnest/signin/'
CLUB_LIST_URL = 'http://127.00.0.1:8000/clubnest/clubs/'
USERNAME = 'sarna'
PASSWORD = '123'

# --- Setup ---
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Increased wait time for element detection
wait = WebDriverWait(driver, 15)
print("WebDriver initialized.")


# --- Helper Functions ---
def smooth_scroll_to_bottom(driver):
    """Scrolls to the bottom of the page in many small, slow steps for visual smoothness."""
    # Use 20 steps (5% increment each) with a small pause for very slow, smooth scrolling
    for i in range(1, 21):
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i / 20});")
        time.sleep(0.4)  # Increased pause for slower scroll
    time.sleep(3)  # Extra pause at the end of the scroll
    print("Scrolled smoothly and slowly to the bottom of the page.")


def smooth_scroll_to_element(driver, element):
    """Smoothly scrolls the page until the target element is in view."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(3)  # Increased pause to observe the element arrival


# --- Test Steps ---
try:
    # 1. Open the Club List page
    driver.get(CLUB_LIST_URL)
    print(f"1. Successfully opened the club list page.")
    time.sleep(3)  # Increased initial pause

    # 2. Smoothly scroll through all clubs (First Scroll)
    print("\n2. Smoothly and slowly scrolling to view all clubs...")
    smooth_scroll_to_bottom(driver)
    time.sleep(3)

    # 3. Click the "Login to Join" button on the first club
    print("\n3. Clicking 'Login to Join' to initiate login...")

    login_to_join_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Login to Join']"))
    )

    smooth_scroll_to_element(driver, login_to_join_button)  # Smoothly scroll to the button

    login_to_join_button.click()
    print("'Login to Join' button clicked. Now on the sign-in page.")
    time.sleep(4)  # Increased pause after navigation

    # 4. Perform Login
    print("\n4. Performing Login...")

    # Ensure we are on the login page (for reliability)
    if LOGIN_URL not in driver.current_url:
        driver.get(LOGIN_URL)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    print(f"Entered username '{USERNAME}' and password.")
    time.sleep(3)  # Added pause before click

    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()
    print("Clicked the login button.")

    # 5. Verify login success and return to clubs
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout')))
    print("Login successful! 'Logout' link is visible.")

    # Navigate back to the club list page after login (or let the redirect happen)
    driver.get(CLUB_LIST_URL)
    print("Navigated back to the club list page.")

    # **LONG PAUSE HERE to ensure club data is fully loaded after login**
    time.sleep(6)

    # 6. Smoothly scroll again (Second Scroll)
    print("\n5. Smoothly scrolling again on the club page after login...")
    smooth_scroll_to_bottom(driver)
    time.sleep(3)

    # 7. Perform Search (after login)
    print("\n6. Performing Search and Joining...")
    search_options = ["Math", "Sports", "Cultural", "Drama", "Cyber", "English Language"]
    random_search_query = random.choice(search_options)

    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
    search_box.send_keys(random_search_query)
    print(f"Typed '{random_search_query}' into the search box.")
    time.sleep(3)  # Pause before clicking search

    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form button[type="submit"]')))
    search_button.click()
    print("Clicked the search button. Viewing search results.")
    time.sleep(4)  # Increased pause after search

    # 8. Join the club found by the search
    try:
        # The button is now 'Join Club' because the user is logged in
        join_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Join Club']"))
        )

        smooth_scroll_to_element(driver, join_button)  # Smoothly scroll to the join button

        join_button.click()
        print(f"Successfully clicked 'Join Club' for the searched result.")
        print("Alert should appear: 'Join request sent! Please wait for admin approval.'")

    except Exception:
        print(
            "INFO: Could not find a 'Join Club' button after search. (Either no results, or user already joined/pending).")

    # Wait to observe the final result
    print("\nTest completed. The browser will close in 12 seconds.")
    time.sleep(10)  # Increased final pause

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser has been closed.")