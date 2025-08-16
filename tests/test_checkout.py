import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.usefixtures("driver", "config")
def test_convert_again_button(driver, config):
    base_url = config.get("base_url", "http://localhost:80")
    driver.get(f"{base_url}/")
    shekels_input = driver.find_element(By.NAME, "shekels")
    shekels_input.clear()
    shekels_input.send_keys("100")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    convert_again = driver.find_element(By.ID, "convert-again")
    convert_again.click()
    time.sleep(1)
    assert driver.find_element(By.TAG_NAME, "form") 