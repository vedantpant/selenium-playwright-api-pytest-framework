import pytest
from playwright.sync_api import sync_playwright
import logging
import os

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        yield page

        context.close()
        browser.close()

@pytest.fixture
def logger(request):
    test_name = request.node.name
    worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")

    logs_dir = os.path.join("reports", "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log = logging.getLogger(f"pw-{test_name}-{worker}")
    log.setLevel(logging.INFO)
    log.propagate = False

    if not log.handlers:
        file_path = os.path.join(logs_dir, f"playwright-{worker}.log")
        fh = logging.FileHandler(file_path, mode="a", encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        fh.setFormatter(fmt)
        log.addHandler(fh)

    return log