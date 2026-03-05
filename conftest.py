# conftest.py
import os
import logging
from datetime import datetime

import allure
from allure_commons.types import AttachmentType
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
    return (
        pytestconfig.getoption("--base-url")
        or os.getenv("BASE_URL")
        or "https://www.saucedemo.com"
    )


@pytest.fixture(scope="session")
def run_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------
# Selenium driver fixtures
# ---------------------------
@pytest.fixture
def driver(ui_browser, ui_headless):
    drv = None
    try:
        drv = DriverFactory.create_driver(ui_browser, ui_headless)
        yield drv
    finally:
        if drv:
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
        if not drv:
            return

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        browser = item.funcargs.get("ui_browser", "unknown")
        headless = "headless" if item.funcargs.get("ui_headless", False) else "headed"
        safe_nodeid = item.nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")

        run_id_val = item.funcargs.get("run_id", "run")
        wid = item.funcargs.get("worker_id", "master")

        screenshots_dir = os.path.join("reports", "runs", run_id_val, wid, "screenshots")
        artifacts_dir = os.path.join("reports", "runs", run_id_val, wid, "artifacts", safe_nodeid)

        # ✅ CREATE DIRECTORIES
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(artifacts_dir, exist_ok=True)

        # ✅ SCREENSHOT
        screenshot_path = os.path.join(
            screenshots_dir,
            f"{safe_nodeid}__{browser}__{headless}__{ts}.png",
        )

        try:
            if os.path.exists(screenshot_path):
                allure.attach.file(screenshot_path, name="screenshot", attachment_type=AttachmentType.PNG)
        except Exception:
            pass

        try:
            url_path = os.path.join(artifacts_dir, "url.txt")
            if os.path.exists(url_path):
                allure.attach.file(url_path, name="url", attachment_type=AttachmentType.TEXT)
        except Exception:
            pass

        try:
            html_path = os.path.join(artifacts_dir, "page_source.html")
            if os.path.exists(html_path):
                allure.attach.file(html_path, name="page_source", attachment_type=AttachmentType.HTML)
        except Exception:
            pass

        try:
            console_path = os.path.join(artifacts_dir, "browser_console.log")
            if os.path.exists(console_path):
                allure.attach.file(console_path, name="browser_console", attachment_type=AttachmentType.TEXT)
        except Exception:
            pass


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