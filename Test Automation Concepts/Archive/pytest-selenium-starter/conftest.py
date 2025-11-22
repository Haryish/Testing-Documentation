import os
import time
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# -------- CLI options --------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome|firefox")
    parser.addoption("--headless", action="store_true", help="run in headless mode")
    parser.addoption("--env", action="store", default=None, help="environment from config.yaml -> envs key")

@pytest.fixture(scope="session")
def config(request):
    cfg_path = os.path.join(os.path.dirname(__file__), "resources", "config.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Decide which environment
    env = request.config.getoption("--env") or data.get("default_env", "dev")
    data["_active_env"] = env
    data["_env_cfg"] = data["envs"][env]
    return data

@pytest.fixture
def driver(request, config):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)  # Selenium Manager handles driver
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    base_url = config["_env_cfg"]["base_url"]
    driver.get(base_url)

    yield driver

    driver.quit()

# -------- Screenshot on PASS & FAIL and attach to pytest-html --------
def _take_screenshot(driver, name):
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join("reports", "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}_{ts}.png")
    driver.save_screenshot(path)
    return path

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # run all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Only on test "call" phase (not setup/teardown)
    if rep.when != "call":
        return

    driver = item.funcargs.get("driver", None)
    if driver is None:
        return

    # Always capture for evidence (both pass & fail)
    screenshot_path = _take_screenshot(driver, item.name)

    # Attach into pytest-html if available
    try:
        from pytest_html import extras as html_extras
        extra = getattr(rep, "extra", [])
        extra.append(html_extras.png(screenshot_path))
        rep.extra = extra
    except Exception:
        # If pytest-html not installed, just ignore
        pass
