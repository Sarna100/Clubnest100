from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True  # PDF auto-download
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get("http://127.0.0.1:8000/clubnest/events/")
    time.sleep(2)

    # Click Show Certificate
    try:
        show_cert_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Show Certificate')]")))
        show_cert_btn.click()
        print("Clicked 'Show Certificate'.")
        time.sleep(2)

        # Switch to new tab opened by certificate (if any)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            print("Switched to certificate tab.")

        # Click Download button
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Download Certificate')]")))
        download_btn.click()
        print(f"Clicked 'Download Certificate'. File should download to: {DOWNLOAD_DIR}")
        time.sleep(5)

    except NoSuchElementException:
        print("No 'Show Certificate' or 'Download Certificate' button found.")

finally:
    print("Test completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
