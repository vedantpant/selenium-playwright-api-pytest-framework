# conftest.py
import os
from datetime import datetime
import pytest
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from core.logger import build_logger

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")

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

try:
    from pytest_html import extras as html_extras
except Exception:
    html_extras = None


def _is_xdist_worker(config) -> bool:
    # True when running under xdist worker process
    return hasattr(config, "workerinput")


def _worker_id(config) -> str:
    if _is_xdist_worker(config):
        return config.workerinput.get("workerid", "gw0")
    return "master"


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)  # IMPORTANT: no FileExistsError
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{ts}.png".replace("/", "_").replace("\\", "_")
            path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(path)

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com",
        help="Base URL for UI tests"
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

import pytest
import requests

@pytest.fixture(scope="session")
def api_base_url():
    # If you’re using dummyjson, keep it stable here
    return "https://dummyjson.com"

@pytest.fixture(scope="session")
def api_client(api_base_url):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    s.base_url = api_base_url  # store base url
    yield s
    s.close()

@pytest.fixture
def logger(request, worker_id):
    test_name = request.node.name
    log_file = f"logs/{test_name}--{worker_id}.log"
    return build_logger(test_name, log_file)

