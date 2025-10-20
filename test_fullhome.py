from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# ---------- Functions ----------
def slow_type(element, text, delay=0.2):
    """Types text into an element slowly, character by character."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def human_scroll(driver, distance, duration=3):
    """Scroll the page like a human."""
    total_steps = random.randint(50, 100)
    step_distance = distance / total_steps
    for _ in range(total_steps):
        driver.execute_script(f"window.scrollBy(0, {step_distance + random.uniform(-1, 1)});")
        time.sleep(duration / total_steps + random.uniform(0, 0.05))

def safe_click(driver, element):
    """Scroll element into view and click safely, fallback to JS click."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(0.5)
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)

# ---------- Setup ----------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

# ---------- Open Homepage ----------
driver.get("http://127.0.0.1:8000/clubnest/")
time.sleep(1)
human_scroll(driver, 1000, duration=4)
time.sleep(1)
human_scroll(driver, -800, duration=3)
time.sleep(1)

# ---------- Sign Up ----------
signup_button = driver.find_element(By.LINK_TEXT, "Sign Up")
safe_click(driver, signup_button)
wait.until(EC.presence_of_element_located((By.NAME, "first_name")))

slow_type(driver.find_element(By.NAME, "first_name"), "Mst.Zerin")
slow_type(driver.find_element(By.NAME, "last_name"), "Firdusi")

department_element = driver.find_element(By.NAME, "department")
actions.move_to_element(department_element).click().perform()
Select(department_element).select_by_value("cse")
time.sleep(0.5)

semester_element = driver.find_element(By.NAME, "semester")
actions.move_to_element(semester_element).click().perform()
Select(semester_element).select_by_visible_text("3rd")
time.sleep(0.5)

slow_type(driver.find_element(By.NAME, "email"), "zerin202@mail.com")
slow_type(driver.find_element(By.NAME, "password1"), "1234")
slow_type(driver.find_element(By.NAME, "password2"), "1234")

submit_signup = driver.find_element(By.XPATH, "//button[@type='submit']")
safe_click(driver, submit_signup)
time.sleep(3)

# ---------- Sign In ----------
driver.get("http://127.0.0.1:8000/clubnest/signin/")
wait.until(EC.presence_of_element_located((By.NAME, "username")))

slow_type(driver.find_element(By.NAME, "username"), "zerin202@mail.com")
slow_type(driver.find_element(By.NAME, "password"), "1234")
submit_login = driver.find_element(By.XPATH, "//button[@type='submit']")
safe_click(driver, submit_login)
time.sleep(3)

# ---------- Navigate to Profile ----------
driver.get("http://127.0.0.1:8000/clubnest/profile/")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

edit_profile_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/profile/edit/')]"))
)

current_scroll = driver.execute_script("return window.pageYOffset;")
target_scroll = driver.execute_script(
    "return arguments[0].getBoundingClientRect().top + window.pageYOffset - 100;", edit_profile_link
)
human_scroll(driver, target_scroll - current_scroll, duration=2.5)
time.sleep(random.uniform(0.5, 1.2))
safe_click(driver, edit_profile_link)

# ---------- Edit Profile ----------
# ---------- Edit Profile with Random Data ----------
try:
    print("\n--- Step 3: Navigating to Edit Profile Page ---")
    driver.get('http://127.0.0.1:8000/clubnest/profile/edit/')

    print("Updating form fields with random data...")

    # --- Random First and Last Name ---
    first_names = ["Sarna", "Saba", "Rifat", "Mahfuz", "Maria"]
    last_names = ["Rani", "Bilas", "Islam", "Bhuiya", "Saba"]
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)

    first_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'first_name')))
    first_name_field.clear()
    time.sleep(0.5)
    slow_type(first_name_field, random_first_name)
    print(f"- Updated first name to: '{random_first_name}'")
    time.sleep(1)

    last_name_field = wait.until(EC.presence_of_element_located((By.NAME, 'last_name')))
    last_name_field.clear()
    time.sleep(0.5)
    slow_type(last_name_field, random_last_name)
    print(f"- Updated last name to: '{random_last_name}'")
    time.sleep(1)




    # --- Random Department ---
    department_element = wait.until(EC.element_to_be_clickable((By.NAME, 'department')))
    department_dropdown = Select(department_element)
    all_dept_options = department_dropdown.options[1:]
    random_dept_option = random.choice(all_dept_options)
    department_dropdown.select_by_visible_text(random_dept_option.text)
    print(f"- Randomly selected department: '{random_dept_option.text}'")
    time.sleep(1)

    # --- Random Semester ---
    semester_element = wait.until(EC.element_to_be_clickable((By.NAME, 'semester')))
    semester_dropdown = Select(semester_element)
    all_sem_options = semester_dropdown.options[1:]
    random_sem_option = random.choice(all_sem_options)
    semester_dropdown.select_by_visible_text(random_sem_option.text)
    print(f"- Randomly selected semester: '{random_sem_option.text}'")
    time.sleep(2)

    # --- Submit Form ---
    print("Finding the 'Save Changes' button...")
    save_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(text(), 'Save Changes')]")
    ))
    safe_click(driver, save_button)
    print("Clicked 'Save Changes' button.")

    print("\n✅ Profile updated successfully! Waiting 5 seconds to continue...")
    time.sleep(5)

except Exception as e:
    print(f"\n❌ An error occurred during profile update: {e}")

# ---------- Back to Homepage ----------
driver.get("http://127.0.0.1:8000/clubnest/")
time.sleep(2)

# ---------- Navigate to "Learn More" ----------
learn_more_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Learn More"))
)
safe_click(driver, learn_more_link)
time.sleep(2)

# ---------- FULL PAGE SCROLL (TOP -> BOTTOM -> TOP) ----------
page_height = driver.execute_script("return document.body.scrollHeight")

# ---------- Human-like smooth full page scroll DOWN ----------
current_scroll = 0
page_height = driver.execute_script("return document.body.scrollHeight")

while current_scroll < page_height:
    # Randomize each scroll step slightly (20 to 40 px)
    step = random.randint(20, 40)

    # Scroll by this step
    driver.execute_script(f"window.scrollBy(0, {step});")
    current_scroll += step

    # Random tiny delay between steps for human feel
    time.sleep(0.04 + random.uniform(0, 0.06))

# ---------- Navigate to 'Explore Clubs' ----------
try:
    print("🔍 Looking for 'Explore Clubs' button...")
    explore_clubs_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Explore Clubs"))
    )
    safe_click(driver, explore_clubs_btn)
    print("✅ Navigated to Explore Clubs page successfully!")
    time.sleep(2)

    # ---------- Human-like scroll on Explore Clubs page ----------
    page_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    print("⏳ Scrolling Explore Clubs page slowly...")

    while current_scroll < page_height:
        step = random.randint(20, 40)  # small random step
        driver.execute_script(f"window.scrollBy(0, {step});")
        current_scroll += step
        time.sleep(0.05 + random.uniform(0, 0.05))  # human-like delay

    # Optional: scroll back to top slowly
    human_scroll(driver, -current_scroll, duration=3)
    print("✅ Finished scrolling Explore Clubs page.")

except Exception as e:
    print(f"❌ Failed to open Explore Clubs: {e}")


# ---------- Search, Scroll, and Join Multiple Clubs ----------
try:
    club_list = ["Drama", "Music", "Art", "Photography"]  # <-- list your favorite clubs here

    for search_term in club_list:
        print(f"\n🔍 Searching for: {search_term}")

        # Optional: random delay before searching
        time.sleep(random.uniform(2, 5))

        # Wait for search input box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='search' or @placeholder='Search']")
            )
        )
        search_box.clear()
        time.sleep(random.uniform(0.3, 0.7))
        slow_type(search_box, search_term, delay=0.15)
        search_box.send_keys(u'\ue007')  # Press Enter

        # Wait for results container
        results_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'results') or contains(@class,'clubs-list')]")
            )
        )
        print("✅ Results container found!")

        # Scroll through results slowly
        results_height = driver.execute_script("return arguments[0].scrollHeight", results_section)
        current_scroll = 0
        while current_scroll < results_height:
            step = random.randint(20, 40)
            driver.execute_script(f"arguments[0].scrollBy(0, {step});", results_section)
            current_scroll += step
            time.sleep(0.05 + random.uniform(0, 0.05))

        # Find all Join buttons
        join_buttons = results_section.find_elements(
            By.XPATH, ".//button[contains(text(), 'Join')] | .//a[contains(text(), 'Join')]"
        )
        print(f"Found {len(join_buttons)} Join button(s) for '{search_term}'.")

        # Click each Join button safely
        for btn in join_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                time.sleep(random.uniform(0.5, 1))
                safe_click(driver, btn)
                print("✅ Clicked Join button.")
                time.sleep(random.uniform(1, 2))  # human-like delay
            except Exception as e:
                print(f"⚠️ Failed to click a Join button: {e}")

        # Small delay before next club search
        time.sleep(random.uniform(2, 4))

except Exception as e:
    print(f"❌ Error during search & join: {e}")
