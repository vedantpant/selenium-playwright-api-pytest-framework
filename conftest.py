# conftest.py
import os
import logging
from datetime import datetime

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from core.driverfactory import DriverFactory


# ---------------------------
# base_url (from pytest-base-url plugin)
# ---------------------------

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    # pytest-base-url plugin provides option "base_url" and CLI flag --base-url
    return pytestconfig.getoption("base_url")


# ---------------------------
# Selenium driver fixtures
# ---------------------------

@pytest.fixture
def driver(ui_browser, ui_headless):
    drv = DriverFactory.create_driver(ui_browser, ui_headless)
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver, ui_timeout):
    return WebDriverWait(driver, ui_timeout)


# ---------------------------
# worker id (supports xdist)
# ---------------------------

def _is_xdist_worker(config) -> bool:
    return hasattr(config, "workerinput")


def _get_worker_id(config) -> str:
    if _is_xdist_worker(config):
        return config.workerinput.get("workerid", "gw0")
    return "master"


@pytest.fixture(scope="session")
def worker_id(pytestconfig):
    return _get_worker_id(pytestconfig)


# ---------------------------
# Logger fixture (simple + reliable)
# ---------------------------

@pytest.fixture
def logger(request, worker_id):
    os.makedirs("logs", exist_ok=True)

    test_name = request.node.name
    log_path = os.path.join("logs", f"{test_name}--{worker_id}.log")

    logger = logging.getLogger(f"{test_name}--{worker_id}")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # avoid duplicate console logs

    # remove old handlers (important when running many tests)
    if logger.handlers:
        logger.handlers.clear()

    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger


# ---------------------------
# Screenshot on failure
# ---------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver", None)
        if drv:
            os.makedirs("reports/screenshots", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{item.name}_{ts}.png".replace("/", "_").replace("\\", "_")
            path = os.path.join("reports/screenshots", name)
            drv.save_screenshot(path)


# ---------------------------
# API fixtures (so test run stays green)
# ---------------------------

@pytest.fixture(scope="session")
def api_base_url():
    return "https://dummyjson.com"


@pytest.fixture(scope="session")
def api_client(api_base_url):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    s.base_url = api_base_url
    yield s
    s.close()


def pytest_addoption(parser):
    parser.addoption(
        "--ui-browser",
        action="store",
        default="chrome",
        help="UI browser for Selenium: chrome|firefox|edge",
    )
    parser.addoption(
        "--ui-headless",
        action="store_true",
        default=False,
        help="Run Selenium in headless mode",
    )
    parser.addoption(
        "--ui-timeout",
        action="store",
        type=int,
        default=10,
        help="Default Selenium explicit wait timeout (seconds)",
    )

@pytest.fixture(scope="session")
def ui_browser(pytestconfig):
    return pytestconfig.getoption("--ui-browser").lower()


@pytest.fixture(scope="session")
def ui_headless(pytestconfig):
    return pytestconfig.getoption("--ui-headless")


@pytest.fixture(scope="session")
def ui_timeout(pytestconfig):
    return int(pytestconfig.getoption("--ui-timeout"))