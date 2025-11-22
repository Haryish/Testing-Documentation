import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

@pytest.mark.smoke
def test_valid_login(driver, config):
    lp = LoginPage(driver)
    lp.login(config["_env_cfg"]["username"], config["_env_cfg"]["password"])
    hp = HomePage(driver)
    assert hp.is_loaded(), "Home page was not loaded after login"

@pytest.mark.regression
def test_invalid_login(driver):
    lp = LoginPage(driver)
    lp.login("locked_out_user", "wrong_password")
    # Saucedemo shows an error; we assert home is NOT loaded
    hp = HomePage(driver)
    assert not hp.is_loaded(), "Home page should not load for invalid credentials"
