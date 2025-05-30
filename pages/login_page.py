# login_page.py

from allure import step
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginPageLocators()

    @step("Открыть страницу логина")
    def open(self):
        self.driver.get(f"{self.base_url}/login")
        return self

    @step("Авторизация с email: {email} и паролем: {password}")
    def login(self, email: str, password: str):
        self.fill(self.locators.EMAIL_INPUT, email)
        self.fill(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        return self

    @step("Переход на страницу регистрации")
    def go_to_register(self):
        self.click(self.locators.REGISTER_LINK)
        return self

    @step("Переход на страницу восстановления пароля")
    def go_to_password_restore(self):
        self.click(self.locators.RESTORE_PASSWORD_LINK)
        return self