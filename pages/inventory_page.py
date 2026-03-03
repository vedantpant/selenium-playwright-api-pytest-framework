from selenium.webdriver.common.by import By
from core.base_page import BasePage
import allure

class InventoryPage(BasePage):
    _inventory_container = (By.CLASS_NAME, "inventory_list")
    _add_backpack_btn = (By.ID, "add-to-cart-sauce-labs-backpack")
    _cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def wait_for_inventory(self):
        self.wait_for_presence(self._inventory_container)

    def add_first_item_to_cart(self):
        self.click(self._add_backpack_btn)

    @allure.step("Proceed to checkout")
    def go_to_cart(self):
        self.click(self._cart_link)
