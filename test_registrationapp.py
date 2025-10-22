from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def setup_teardown():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")  # Run in Jenkins
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Automatically get the correct ChromeDriver version for your Chrome
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    yield driver
    driver.quit()


# Helper to get alert text safely
def get_alert_text(driver):
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text

# Test 1: Empty username
def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."

# Test 2: Empty password
def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("John Doe")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."

# Test 3: Password too short
def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."

# Test 4: Valid input — should redirect to greeting.html
def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()

    # Wait for redirect and body text
    WebDriverWait(driver, 5).until(
        EC.url_contains("/result")
    )

    current_url = driver.current_url
    assert "/result" in current_url, f"Expected redirect to greeting.html, but got: {current_url}"

    body_text = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    ).text
    assert "Hello, Alice! Welcome to the website" in body_text, f"Greeting not found or incorrect: {body_text}"
