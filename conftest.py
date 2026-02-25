# conftest.py
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait



@pytest.fixture(scope="session")
def base_url(pytestconfig):
    # pytest-base-url plugin exposes it as config option
    return pytestconfig.getoption("base_url")


# ---------------------------
# DRIVER FIXTURE
# ---------------------------

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


# ---------------------------
# SCREENSHOT ON FAILURE
# ---------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            path = os.path.join("reports/screenshots", file_name)
            driver.save_screenshot(path)