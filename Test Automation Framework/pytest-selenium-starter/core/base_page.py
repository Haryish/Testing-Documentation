from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def wait_for(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait_for(locator).click()

    def type(self, locator, text):
        el = self.wait_for(locator)
        el.clear()
        el.send_keys(text)

    def is_visible(self, locator):
        try:
            self.wait_for(locator)
            return True
        except Exception:
            return False
