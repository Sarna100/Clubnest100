import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- Configuration ---
ABOUT_URL = 'http://127.0.0.1:8000/clubnest/about-us/'
SPONSOR_URL = 'http://127.0.0.1:8000/clubnest/sponsors/'
# Assuming your Django Home page URL is the root of the app
HOME_URL = 'http://127.0.0.1:8000/clubnest/'

# --- Setup ---
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)
print("WebDriver initialized successfully.")


# --- Helper Functions ---
def smooth_scroll_to_bottom(driver):
    """Scrolls to the bottom of the page in steps for visual smoothness."""
    for i in range(1, 11):
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i / 10});")
        time.sleep(0.3)  # Small pause between scroll steps
    time.sleep(3)
    print("Scrolled smoothly to the bottom of the page.")


def smooth_scroll_to_element(driver, element):
    """Smoothly scrolls the page until the target element is in view."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(3)


# --- Test Steps ---
try:
    # 1. Navigate to the About Page
    driver.get(ABOUT_URL)
    print(f"1. Successfully opened the About page: {ABOUT_URL}")
    time.sleep(2)

    # 2. Find and hover over the 'More' dropdown
    print("\n2. Finding and hovering over the 'More' dropdown...")
    more_dropdown_parent = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dropdown'))
    )

    # Hover action is needed to make the dropdown links visible
    ActionChains(driver).move_to_element(more_dropdown_parent).perform()
    time.sleep(1.5)  # Pause to let the dropdown animation complete

    # 3. Find and click the 'Sponsors' link within the dropdown
    print("3. Clicking the 'Sponsors' link...")
    sponsors_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-content']/a[text()='Sponsors']"))
    )

    sponsors_link.click()
    print("Successfully clicked 'Sponsors'. Navigating to the Sponsors page.")

    # Wait for the Sponsors page to fully load
    wait.until(EC.url_to_be(SPONSOR_URL))
    time.sleep(3)

    # 4. Scroll the Sponsors page
    print("\n4. Scrolling the Sponsors page to view all content...")
    smooth_scroll_to_bottom(driver)

    # --- NEW STEP: GO BACK TO HOME ---
    print("\n5. Test finished. Navigating back to the Home page...")
    driver.get(HOME_URL)
    wait.until(EC.url_to_be(HOME_URL))
    print(f"Successfully landed on the Home page: {HOME_URL}")
    # --- END OF NEW STEP ---

    # 6. Wait to observe the final result
    print("\nTest completed. The browser will close in 7 seconds.")
    time.sleep(7)

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    # --- Teardown ---
    driver.quit()
    print("Browser has been closed.")