import pytest
import lib.LoginCreds as LoginCreds
from lib.Constants import CHROME_MOBILE, CHROME_HEADLESS
from pages.CartPage import CartPage
from pages.LoginPage import LoginPage
from pages.ProductListPage import ProductListPage
from pages.CheckoutPage import CheckoutPage
from pages.OverviewPage import OverviewPage


@pytest.mark.parametrize(
    "browser,mode,device, username, password",
    [
        (*CHROME_MOBILE, LoginCreds.TEST_USER, LoginCreds.STANDARD_PASSWORD),
        (*CHROME_HEADLESS, LoginCreds.TEST_USER, LoginCreds.STANDARD_PASSWORD),
    ],
)
@pytest.mark.checkout
def test_information_input(driver, browser, mode, device, username, password):
    # Proceed to checkout page
    login_page = LoginPage(driver)
    login_page.perform_complete_login(username, password)
    product_page = ProductListPage(driver)
    product_page.click_cart()
    cart_page = CartPage(driver)
    cart_page.click_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.click_continue()
    assert checkout_page.is_error_message_present()

    first_name = "Adria"
    last_name = "Aprilia"
    postal_code = "45216"
    checkout_page.input_first_name(first_name)
    checkout_page.input_last_name(last_name)
    checkout_page.input_postal_code(postal_code)
    checkout_page.input_payment_details()

    assert checkout_page.get_first_name() == first_name
    assert checkout_page.get_last_name() == last_name
    assert checkout_page.get_postal_code() == postal_code
    checkout_page.click_continue()
    overview_page = OverviewPage(driver)
    assert overview_page.get_subheader() == "Checkout: Overview"

@pytest.mark.parametrize(
    "browser,mode,device, username, password",
    [
        (*CHROME_MOBILE, LoginCreds.TEST_USER, LoginCreds.STANDARD_PASSWORD),
        (*CHROME_HEADLESS, LoginCreds.TEST_USER, LoginCreds.STANDARD_PASSWORD),
    ],
)
@pytest.mark.checkout
def test_cancel_button(driver, browser, mode, device, username, password):
    login_page = LoginPage(driver)
    login_page.perform_complete_login(username, password)
    product_page = ProductListPage(driver)
    product_page.click_cart()
    cart_page = CartPage(driver)
    cart_page.click_checkout()
    checkout_page = CheckoutPage(driver)
    checkout_page.click_cancel()
    assert cart_page.get_subheader() == "Your Cart"
