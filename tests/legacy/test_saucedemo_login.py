from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.mark.skip(reason="legacy scratch test")
def test_sauce_demo_login():

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.saucedemo.com")

    #login
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # validate inventory loaded
    inventory_item = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    print("Inventory loaded successfully")

    # add first item to the cart
    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_inventory")))
    add_to_cart_button.click()

    cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

    assert cart_badge.text == "1"
    print("Item added to cart successfully")


    driver.quit()