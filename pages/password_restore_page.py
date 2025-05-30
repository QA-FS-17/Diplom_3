# password_restore_page.py

from allure import step
from .base_page import BasePage
from locators.password_restore_locators import PasswordRestoreLocators

class PasswordRestorePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PasswordRestoreLocators()

    @step("Открыть страницу восстановления пароля")
    def open(self):
        self.driver.get(f"{self.base_url}/forgot-password")
        return self

    @step("Восстановить пароль для email: {email}")
    def restore_password(self, email: str):
        self.fill(self.locators.EMAIL_INPUT, email)
        self.click(self.locators.RESTORE_BUTTON)
        return self

    @step("Переключить видимость пароля")
    def toggle_password_visibility(self):
        self.click(self.locators.SHOW_HIDE_BUTTON)
        return self

    @step("Проверить активность поля ввода")
    def is_input_active(self) -> bool:
        return self.is_visible(self.locators.INPUT_ACTIVE)