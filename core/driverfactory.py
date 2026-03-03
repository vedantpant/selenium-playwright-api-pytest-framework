from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


class DriverFactory:
    @staticmethod
    def create_driver(browser: str= "chrome", headless: bool = False):
        browser = browser.lower()

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

            return webdriver.Chrome(options=options)

        if browser == "firefox":
            from selenium.webdriver.firefox.options import Options as FFOptions

            options = FFOptions()
            if headless:
                options.add_argument("--headless")
            drv = webdriver.Firefox(options=options)
            drv.maximize_window()
            return drv

        if browser == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions

            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
                drv = webdriver.Edge(options=options)
                drv.maximize_window()
                return drv

        raise ValueError(f"Unsupported browser: {browser}")

