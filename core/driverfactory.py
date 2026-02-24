from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core.config import Config

class DriverFactory:

    @staticmethod
    def create_driver():
        if Config.BROWSER == 'chrome':
            options = Options()

            if Config.HEADLESS:
                options.add_argument('--headless=new')

            options.add_argument("--start-maximized")

            driver =webdriver.Chrome(options=options)
            driver.implicitly_wait(0)
            return driver

        raise Exception(f"Unsupported browser: {Config.BROWSER}")