from logging import Logger

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.selenium
@pytest.mark.flaky
def test_add_to_cart(driver,base_url, logger):

    login_page = LoginPage(driver,logger)
    inventory_page = InventoryPage(driver,logger)
    cart_page = CartPage(driver,logger)

    login_page.load(base_url)
    login_page.login("standard_user","secret_sauce")

    inventory_page.wait_for_inventory()
    inventory_page.add_first_item_to_cart()
    inventory_page.go_to_cart()

    #cart_page.wait_for_cart_item()
    assert cart_page.has_items()
    # assert False

    driver.quit()

