from selenium.webdriver.common.by import By
from core.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class CartPage(BasePage):
    _cart_title = (By.CLASS_NAME, "title")
    _cart_item = (By.CLASS_NAME, "cart_item")

    def wait_for_cart_item(self):
        self.wait_for_visible(self._cart_title)
        self.wait_for_presence(self._cart_item)


    def has_items(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*self._cart_item)) > 0
            )
            return True
        except TimeoutException:
            return False
