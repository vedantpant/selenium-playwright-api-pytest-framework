import pytest

@pytest.mark.ui
@pytest.mark.playwright
def test_add_to_cart_playwright(page):

    page.goto("https://www.saucedemo.com")

    #login
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    #Auto-wait happens here
    page.wait_for_selector(".inventory_list")

    #add item to cart
    page.click("#add-to-cart-sauce-labs-backpack")

    #Go to cart
    page.click(".shopping_cart_link")

    #Assertion
    page.wait_for_selector(".cart_item")
    assert page.locator(".cart_item").count() > 0

@pytest.mark.ui
@pytest.mark.playwright
def test_api_and_ui_playwright(page):

    response = page.request.get(
        "https://jsonplaceholder.typicode.com/users/1"
    )

    assert response.status == 200

    user = response.json()
    assert user["id"] == 1

    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    page.wait_for_selector(".inventory_list")
