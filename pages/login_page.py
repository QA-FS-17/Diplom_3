# login_page.py

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    RESTORE_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")

    def go_to_site(self):
        self.driver.get(self.base_url)

    def click_restore_password_link(self):
        self.click_element(self.RESTORE_PASSWORD_LINK)
        self.wait_for_url_contains("forgot-password")