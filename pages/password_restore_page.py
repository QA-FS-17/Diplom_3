# password_restore_page.py

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from locators.password_restore_locators import PasswordRestoreLocators
from .base_page import BasePage
from selenium.webdriver.common.by import By


class ForgotPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PasswordRestoreLocators()

    def go_to_site(self, path=""):
        self.driver.get(f"{self.base_url}{path}")
        self._wait(self.locators.EMAIL_INPUT)

    def enter_email(self, email: str):
        self.fill_field(self.locators.EMAIL_INPUT, email)

    def submit_form(self):
        self.click_element(self.locators.SUBMIT_BUTTON)

    def toggle_password_visibility(self):
        eye_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locators.SHOW_HIDE_BUTTON)
        )
        ActionChains(self.driver).move_to_element(eye_icon).click().perform()

    def is_field_highlighted(self):
        field = self.driver.find_element(*self.locators.PASSWORD_FIELD)
        parent = field.find_element(By.XPATH, "./..")

        parent_classes = parent.get_attribute("class")
        border_color = parent.value_of_css_property("border-color")

        return (
                "active" in parent_classes or
                "focused" in parent_classes or
                "highlight" in parent_classes or
                "rgb(255, 0, 0)" in border_color or
                "red" in border_color.lower()
        )

    def is_element_present(self, locator, timeout=None):
        try:
            self._wait(locator, timeout or self.default_timeout)
            return True
        except:
            return False