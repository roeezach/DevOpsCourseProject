import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.usefixtures("driver", "config")
def test_convert_usd(driver, config):
    base_url = config.get("base_url", "http://localhost:80")
    driver.get(f"{base_url}/")
    shekels_input = driver.find_element(By.NAME, "shekels")
    shekels_input.clear()
    shekels_input.send_keys("100")
    select = driver.find_element(By.NAME, "currency")
    for option in select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == "usd":
            option.click()
            break
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    result = driver.find_element(By.ID, "result")
    assert "$" in result.text and "27.00" in result.text

@pytest.mark.usefixtures("driver", "config")
def test_convert_eur(driver, config):
    base_url = config.get("base_url", "http://localhost:80")
    driver.get(f"{base_url}/")
    shekels_input = driver.find_element(By.NAME, "shekels")
    shekels_input.clear()
    shekels_input.send_keys("100")
    select = driver.find_element(By.NAME, "currency")
    for option in select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == "eur":
            option.click()
            break
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    result = driver.find_element(By.ID, "result")
    assert "€" in result.text and "25.00" in result.text

@pytest.mark.usefixtures("driver", "config")
def test_convert_gbp(driver, config):
    base_url = config.get("base_url", "http://localhost:80")
    driver.get(f"{base_url}/")
    shekels_input = driver.find_element(By.NAME, "shekels")
    shekels_input.clear()
    shekels_input.send_keys("100")
    select = driver.find_element(By.NAME, "currency")
    for option in select.find_elements(By.TAG_NAME, "option"):
        if option.get_attribute("value") == "gbp":
            option.click()
            break
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    result = driver.find_element(By.ID, "result")
    assert "£" in result.text and "21.00" in result.text 