import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.selenium
def test_scroll_to_bottom(driver, logger):

    driver.get("https://the-internet.herokuapp.com/large")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    scroll_position = driver.execute_script("return window.pageYOffset;")

    assert scroll_position > 0


@pytest.mark.ui
@pytest.mark.selenium
def test_scroll_into_view(driver, logger):
    driver.get("https://the-internet.herokuapp.com/large")

    # Pick something guaranteed: the last row/col cell
    target_locator = (By.XPATH, "(//table[@id='large-table']//tr[last()]/td[last()])[1]")

    wait = WebDriverWait(driver, 10)
    target = wait.until(EC.presence_of_element_located(target_locator))

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)

    # sanity check: it's interactable/visible-ish
    assert target.is_displayed()