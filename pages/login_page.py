# login_page.py

from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators

class LoginPage(BasePage):
    LOGIN_URL = "login"  # относительный путь

    def go_to_login_page(self):
        """Явно открывает страницу логина"""
        self.driver.get(self.base_url + self.LOGIN_URL)

    def click_restore_password_link(self):
        """Клик по ссылке восстановления пароля"""
        self.click_element(LoginPageLocators.RESTORE_PASSWORD_LINK)
        self.wait_for_url_contains("forgot-password")

    def login(self, email, password):
        """
        Полный процесс авторизации
        :param email: Email пользователя
        :param password: Пароль пользователя
        """
        self.fill_field(LoginPageLocators.EMAIL_INPUT, email)
        self.fill_field(LoginPageLocators.PASSWORD_INPUT, password)
        self.click_element(LoginPageLocators.LOGIN_BUTTON)
        self.wait_for_url_contains("/")  # Проверяем переход на главную

    def click_register_link(self):
        """Клик по ссылке регистрации"""
        self.click_element(LoginPageLocators.REGISTER_LINK)
        self.wait_for_url_contains("register")

    def should_be_login_page(self):
        """Проверка, что мы на странице логина"""
        assert "login" in self.driver.current_url
        assert self.is_element_present(LoginPageLocators.LOGIN_BUTTON), "Кнопка входа не найдена"