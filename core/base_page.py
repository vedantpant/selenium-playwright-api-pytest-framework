from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from core.config import Config
import time

class BasePage:

    def __init__(self, driver,logger=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.logger = logger

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

    # =========================
    # SAFE CLICK
    # =========================
    def click(self, locator, retries=2):
        self._log(f"Clicking element: {locator}")
        for attempt in range(retries):
            try:
                element = self.wait.until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return
            except ElementClickInterceptedException:
                self._log("Click intercepted, trying scroll + retry")
                self.scroll_into_view(locator)
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                time.sleep(0.5)

    # =========================
    # SAFE TYPE
    # =========================
    def type(self, locator, text, retries=2):
        self._log(f"Typing into element: {locator}")
        for attempt in range(retries):
            try:
                element = self.wait.until(
                    EC.visibility_of_element_located(locator)
                )
                element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise

    # =========================
    # GET TEXT
    # =========================
    def get_text(self, locator):
        self._log(f"Getting text from element: {locator}")
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    # =========================
    # SCROLL
    # =========================
    def scroll_into_view(self, locator):
        self._log(f"Clicking element: {locator}")
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

    # =========================
    # URL WAIT
    # =========================
    def wait_for_url_contains(self, value):
        self._log(f"waiting for url to contain: {value}. Current={self.driver.current_url}")
        self.wait.until(EC.url_contains(value))

    # =========================
    # WINDOW HANDLING
    # =========================
    def switch_to_new_window(self):
        current = self.driver.current_window_handle
        self.wait.until(lambda d: len(d.window_handles) > 1)
        for handle in self.driver.window_handles:
            if handle != current:
                self.driver.switch_to.window(handle)
                break

    def switch_to_parent_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    # =========================
    # FRAME HANDLING
    # =========================
    def switch_to_frame(self, locator):
        frame = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        self.driver.switch_to.frame(frame)

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    # =========================
    # CUSTOM WAITS
    # =========================
    def wait_for_presence(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator):
        self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_count(self, locator, count):
        self.wait.until(
            lambda d: len(d.find_elements(*locator)) == count
        )
