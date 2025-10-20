import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------
# Helper Function: Slow Typing
# ------------------------------
def slow_type(element, text, delay=0.15):
    """Type characters one by one with delay"""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# ------------------------------
# Setup
# ------------------------------
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # 1️⃣ Open signup page
    driver.get('http://127.0.0.1:8000/clubnest/signup/')
    print("✅ Opened signup page.")
    time.sleep(2)

    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"johndoe_{timestamp}@example.com"
    print(f"Generated unique email for this test: {unique_email}")

    # 2️⃣ Fill the form slowly
    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'first_name')))
    slow_type(first_name_field, "John")

    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'last_name')))
    slow_type(last_name_field, "Doe")
    print("🖊 Filled first & last name slowly.")

    # Department
    department_select_element = wait.until(EC.presence_of_element_located((By.NAME, 'department')))
    Select(department_select_element).select_by_value('cse')
    print("🎓 Selected Department: CSE")

    # Semester
    semester_select_element = wait.until(EC.presence_of_element_located((By.NAME, 'semester')))
    Select(semester_select_element).select_by_visible_text('3rd')
    print("📘 Selected Semester: 3rd")

    # Email
    email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    slow_type(email_field, unique_email)
    print("📧 Typed email slowly.")

    # Password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password1')))
    slow_type(password_field, "MySecurePassword123")

    confirm_password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password2')))
    slow_type(confirm_password_field, "MySecurePassword123")
    print("🔒 Typed password slowly.")

    time.sleep(1)

    # 3️⃣ Submit the form
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=\"submit\"]')))
    submit_button.click()
    print("✅ Clicked 'Sign Up' button.")

    # 4️⃣ Pause to observe
    print("🕐 Test completed. The browser will close in 10 seconds.")
    time.sleep(10)

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    driver.quit()
    print("🚪 Browser closed.")
