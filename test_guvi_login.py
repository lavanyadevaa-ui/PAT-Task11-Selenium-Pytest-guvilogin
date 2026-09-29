import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver():
    d = webdriver.Chrome()   # no Service or Options
    yield d
    d.quit()


def test_input_fields(driver):
    driver.get("https://www.guvi.in/sign-in/")
    u = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
    p = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
    u.send_keys("lavanyadevaa@gmail.com")
    p.send_keys("Hasmith@123003")
    assert u.is_enabled() and p.is_enabled()

def test_submit_button(driver):
    driver.get("https://www.guvi.in/sign-in/")
    driver.find_element(By.ID, "email").send_keys("lavanyadevaa@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Hasmith@123003")
    btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-btn")))
    btn.click()
    time.sleep(2)

def test_invalid_login(driver):
    driver.get("https://www.guvi.in/sign-in/")
    driver.find_element(By.ID, "email").send_keys("wrong_user@example.com")
    driver.find_element(By.ID, "password").send_keys("wrong_pass")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    time.sleep(2)
    try:
        err = driver.find_element(By.CLASS_NAME, "invalid-feedback")
        assert err.is_displayed()
    except NoSuchElementException:
        pytest.fail("No error message for invalid login")

def test_empty_fields(driver):
    driver.get("https://www.guvi.in/sign-in/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    time.sleep(2)
    assert driver.current_url == "https://www.guvi.in/sign-in/"
