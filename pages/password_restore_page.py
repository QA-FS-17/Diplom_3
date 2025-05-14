# password_restore_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ForgotPasswordPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Инструкции отправлены')]")
    SHOW_HIDE_BUTTON = (By.CSS_SELECTOR, "div.input__icon > svg")

    def go_to_site(self, path=""):
        self.driver.get(f"{self.base_url}{path}")
        self._wait(self.EMAIL_INPUT)

    def enter_email(self, email: str):
        self.fill_field(self.EMAIL_INPUT, email)

    def submit_form(self):
        self.click_element(self.SUBMIT_BUTTON)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
        )

    def is_success_message_displayed(self) -> bool:
        return self.is_element_present(self.SUCCESS_MESSAGE)

    def toggle_password_visibility(self):
        self.click_element(self.SHOW_HIDE_BUTTON)

    def is_password_field_highlighted(self) -> bool:
        return "input_status_active" in self._wait(self.EMAIL_INPUT).get_attribute("class")