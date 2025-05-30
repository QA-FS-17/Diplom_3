# register_page.py

from allure import step
from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = RegisterPageLocators()

    @step("Открыть страницу регистрации")
    def open(self):
        self.driver.get(f"{self.base_url}/register")
        return self

    @step("Зарегистрировать пользователя: {name}, {email}")
    def register(self, name: str, email: str, password: str):
        self.fill(self.locators.NAME_INPUT, name)
        self.fill(self.locators.EMAIL_INPUT, email)
        self.fill(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.REGISTER_BUTTON)
        return self

    @step("Проверить наличие сообщения об ошибке")
    def should_have_error_message(self, expected_message: str):
        actual_message = self.driver.find_element(*self.locators.ERROR_MESSAGE).text
        assert expected_message in actual_message, \
            f"Ожидалось сообщение '{expected_message}', но получено '{actual_message}'"

    @step("Перейти на страницу входа")
    def go_to_login(self):
        self.click(self.locators.LOGIN_LINK)
        return self