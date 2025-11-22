from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    INVENTORY = (By.CLASS_NAME, "inventory_list")

    def is_loaded(self):
        return self.is_visible(self.INVENTORY)
