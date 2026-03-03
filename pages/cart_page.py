from selenium.webdriver.common.by import By
from core.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class CartPage(BasePage):
    _cart_title = (By.CLASS_NAME, "title")
    _cart_item = (By.CLASS_NAME, "cart_item")

    @allure.step("Wait for cart page and cart item")
    def wait_for_cart_item(self, timeout=10):
        # ✅ ensure navigation really happened
        WebDriverWait(self.driver, timeout).until(EC.url_contains("cart.html"))

        self.wait_for_visible(self._cart_title)
        self.wait_for_presence(self._cart_item)

    @allure.step("Verify items present in cart")
    def has_items(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*self._cart_item)) > 0
            )
            return True
        except TimeoutException:
            return False
