from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# === User credentials ===
USER_EMAIL = "mohona123@gmail.com"
USER_PASSWORD = "123"
NEW_PROFILE_NAME = "Sarna New"

# === Browser Setup ===
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
time.sleep(1)

# === Django Local Server Home URL ===
home_url = "http://127.0.0.1:8000/clubnest/"

# === Step 1: Go to Home Page ===
driver.get(home_url)
print("✅ Opened Home Page ->", driver.current_url)
time.sleep(2)

# === Step 2: Sign Up ===
try:
    driver.find_element(By.LINK_TEXT, "Sign Up").click()
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "email").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password1").send_keys(USER_PASSWORD)
    driver.find_element(By.NAME, "password2").send_keys(USER_PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(3)
    print("✅ User signed up successfully.")
except Exception as e:
    print("❌ Sign Up failed:", e)

# === Step 3: Sign In ===
try:
    driver.find_element(By.LINK_TEXT, "Sign in").click()
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Sign In']").click()
    time.sleep(2)
    print("✅ User signed in successfully.")
except Exception as e:
    print("❌ Sign in failed:", e)

# === Step 4: Profile Edit ===
try:
    driver.find_element(By.XPATH, "//img[@class='profile-img']").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Edit Profile").click()
    time.sleep(2)
    name_input = driver.find_element(By.NAME, "full_name")
    name_input.clear()
    name_input.send_keys(NEW_PROFILE_NAME)
    driver.find_element(By.XPATH, "//button[text()='Save']").click()
    time.sleep(2)
    print("✅ Profile edited successfully.")
except Exception as e:
    print("❌ Profile edit failed:", e)

# === Step 5: Visit all Navbar Pages sequentially ===
nav_links = [
    ("Home", home_url),
    ("About", "http://127.0.0.1:8000/clubnest/about-us/"),
    ("Events", "http://127.0.0.1:8000/clubnest/events/"),
    ("club", "http://127.0.0.1:8000/club_list/")
]

for name, url in nav_links:
    try:
        driver.get(home_url)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, name).click()
        time.sleep(2)
        print(f"✅ '{name}' page opened ->", driver.current_url)

        # === Club Page Join Button ===
        if name.lower() == "club":
            try:
                join_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Join')]")
                join_btn.click()
                time.sleep(2)
                print("✅ Club Join button clicked.")
            except Exception as e:
                print("❌ Club Join button failed:", e)

        # === Events Page Join Button ===
        if name.lower() == "events":
            try:
                join_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Join')]")
                join_btn.click()
                time.sleep(2)
                print("✅ Event Join button clicked.")
            except Exception as e:
                print("❌ Event Join button failed:", e)

    except Exception as e:
        print(f"❌ '{name}' page test failed:", e)

# === Step 6: Hero Section Learn More button test ===
try:
    driver.get(home_url)
    time.sleep(1)
    learn_btn = driver.find_element(By.LINK_TEXT, "Learn More")
    learn_btn.click()
    time.sleep(2)
    print("✅ 'Learn More' button works ->", driver.current_url)
except Exception as e:
    print("❌ 'Learn More' button test failed:", e)

# === Quit Browser ===
driver.quit()
print("Test completed.")
