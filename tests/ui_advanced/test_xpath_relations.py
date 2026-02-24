import pytest
from selenium.webdriver.common.by import By

@pytest.mark.ui
@pytest.mark.selenium
def test_dynamic_add_remove(driver, wait):

    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")

    add_button = (By.XPATH, "//button[text()='Add Element']")
    delete_locator = (By.XPATH, "//div[@id='elements']//button[text()='Delete']")

    for _ in range(5):
        driver.find_element(*add_button).click()

    delete_buttons = driver.find_elements(*delete_locator)
    assert len(delete_buttons) == 5

    delete_buttons[0].click()
    delete_buttons[1].click()

    remaining = driver.find_elements(*delete_locator)
    assert len(remaining) == 3


