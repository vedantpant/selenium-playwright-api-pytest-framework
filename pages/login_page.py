from selenium.webdriver.common.by import By
from core.base_page import BasePage
import allure

class LoginPage(BasePage):

    #locators
    _username = (By.ID, 'user-name')
    _password = (By.ID, 'password')
    _login_btn = (By.ID, 'login-button')

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def load(self, base_url):
        assert base_url, "base_url is empty/None. Set it in pytest.ini or pass --base-url"
        self.driver.get(base_url)

    @allure.step("Login with username: {username}")
    def login(self, username, password):
        self.type(self._username, username)
        self.type(self._password, password)
        self.click(self._login_btn)
