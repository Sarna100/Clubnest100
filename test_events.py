from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- User Credentials ---
USER_EMAIL = "mohona123@gmail.com"
USER_PASSWORD = "123"

# --- Event Page URL ---
EVENTS_URL = "http://127.0.0.1:8000/clubnest/events/"

# --- Setup WebDriver ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:

    driver.get(EVENTS_URL)
    print("Opened Events page.")
    time.sleep(2)


    try:
        login_button = driver.find_element(By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Signin')]")
        login_button.click()
        print("Clicked Login button.")

        # Wait for login form
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USER_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Logged in successfully.")
        time.sleep(2)


        driver.get(EVENTS_URL)
        print("Returned to Events page after login.")
        time.sleep(2)

    except NoSuchElementException:
        print("Already logged in, no login needed.")


    events = driver.find_elements(By.CSS_SELECTOR, ".event-item")
    print(f"Total events found: {len(events)}")

    for idx, event in enumerate(events, 1):
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", event)
        time.sleep(1)  # wait for smooth scroll

        # --- Join Event ---
        try:
            join_btn = event.find_element(By.XPATH, ".//a[contains(text(),'Join Event')]")
            join_btn.click()
            print(f"[{idx}] Joined Event successfully.")
            time.sleep(2)
        except NoSuchElementException:
            # --- Show Certificate ---
            try:
                cert_btn = event.find_element(By.XPATH, ".//a[contains(text(),'Show Certificate')]")
                cert_btn.click()
                print(f"[{idx}] Opened Certificate.")
                time.sleep(2)
                driver.back()  # Return to events page after viewing certificate
            except NoSuchElementException:
                print(f"[{idx}] No action button for this event.")

finally:
    print("Test completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
