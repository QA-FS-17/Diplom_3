# login_page.py

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    RESTORE_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")
    LOGIN_URL = "login"  # относительный путь

    def go_to_login_page(self):
        """Явно открывает страницу логина"""
        self.driver.get(self.base_url + self.LOGIN_URL)

    def click_restore_password_link(self):
        self.click_element(self.RESTORE_PASSWORD_LINK)
        self.wait_for_url_contains("forgot-password")