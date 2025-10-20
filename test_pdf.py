from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# ==========================
# User Credentials
# ==========================
USER_EMAIL = "mohona123@gmail.com"
USER_PASSWORD = "123"

# ==========================
# Event / Certificate Page URL
# ==========================
CERTIFICATE_URL = "http://127.0.0.1:8000/clubnest/certificate/9/"

# ==========================
# Download Folder Path
# ==========================
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")  # Project folder-এর মধ্যে downloads folder
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ==========================
# Chrome Options
# ==========================
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True  # PDF browser এ না খুলে ডাউনলোড হবে
}

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)

# ==========================
# Setup WebDriver
# ==========================
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # ==========================
    # Open Certificate Page
    # ==========================
    driver.get(CERTIFICATE_URL)
    print("Opened Certificate page.")
    time.sleep(2)

    # ==========================
    # Login Handling
    # ==========================
    try:
        login_button = driver.find_element(By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Signin')]")
        login_button.click()
        print("Clicked Login button.")

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USER_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Logged in successfully.")
        time.sleep(2)

        # After login, go back to Certificate page
        driver.get(CERTIFICATE_URL)
        time.sleep(2)
        print("Returned to Certificate page after login.")

    except NoSuchElementException:
        print("Already logged in, no login needed.")

    # ==========================
    # Click Show Certificate (if button exists)
    # ==========================
    try:
        show_cert_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Show Certificate')]")
        show_cert_btn.click()
        print("Clicked Show Certificate button.")
        time.sleep(2)
    except NoSuchElementException:
        print("Show Certificate button not found, already on certificate page.")

    # ==========================
    # Click Download Certificate PDF
    # ==========================
    try:
        download_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Download Certificate')]")
        download_btn.click()
        print(f"Download button clicked. PDF will be saved to: {DOWNLOAD_DIR}")
        time.sleep(5)  # wait for download to complete
    except NoSuchElementException:
        print("Download button not found.")

finally:
    print("Test completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
