import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

# --- Smooth scroll helper ---
def smooth_scroll(driver, pixels=300, delay=0.5):
    """Scroll down smoothly by small steps."""
    current = 0
    while current < pixels:
        driver.execute_script(f"window.scrollBy(0, 50);")
        time.sleep(delay)
        current += 50

# --- Valid social link checker ---
def is_valid_social(url):
    if not url:
        return False
    url = url.lower()
    return any(s in url for s in ["facebook.com", "linkedin.com", "github.com"])

# --- Setup WebDriver ---
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:8000/clubnest/about-us/")
driver.maximize_window()
time.sleep(2)

# --- Smoothly scroll to the team section ---
print("🪄 Scrolling smoothly to team section...")
smooth_scroll(driver, pixels=1500, delay=0.2)
time.sleep(1)

team_section = driver.find_element(By.CLASS_NAME, "team-section")
driver.execute_script("arguments[0].scrollIntoView(true);", team_section)
time.sleep(2)

# --- Get all team members ---
team_members = driver.find_elements(By.CSS_SELECTOR, ".team-member")
print(f"Found {len(team_members)} total team members.\n")

# --- Pick 3 random members ---
selected_members = random.sample(team_members, min(3, len(team_members)))

# --- Loop through 3 random members ---
for idx, member in enumerate(selected_members, start=1):
    print(f"🧩 Profile {idx}:")

    # Smooth scroll to each member
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", member)
    time.sleep(2)

    name = member.find_element(By.CSS_SELECTOR, ".member-info h4").text
    print(f"   👤 {name}")

    # Get social links
    social_links = member.find_elements(By.CSS_SELECTOR, ".member-social a")

    for link in social_links:
        href = link.get_attribute("href")
        icon = link.find_element(By.TAG_NAME, "i").get_attribute("class")

        # ✅ Open only valid social links
        if is_valid_social(href):
            try:
                driver.execute_script(f"window.open('{href}', '_blank');")
                print(f"   ✅ Opened {icon} in new tab → {href}")
                time.sleep(1.5)
            except Exception as e:
                print(f"   ❌ Failed to open {icon}: {e}")
        else:
            print(f"   ⚠️ Skipping {icon} — Not a valid social URL ({href})")

    print("-" * 80)
    time.sleep(2)

# --- Pause for 30 seconds before closing ---
print("\n⏸️ Pausing for 30 seconds so you can view all opened tabs...")
time.sleep(30)

# --- Close browser ---
driver.quit()
print("✅ Done! Browser closed successfully.")
