# password_restore_page.py

import allure
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
from locators.password_restore_locators import PasswordRestoreLocators
from config import config


class PasswordRestorePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, config.FORGOT_PASSWORD_URL)
        self.locators = PasswordRestoreLocators()

    @allure.step("Открыть страницу восстановления пароля")
    def open(self) -> None:
        """Открывает страницу и проверяет ее загрузку"""
        super().open()
        self.is_visible(self.locators.RESTORE_FORM)

    @allure.step("Ввести email")
    def enter_email(self, email: str) -> None:
        """Вводит email в поле восстановления пароля"""
        element = self.wait_until_visible(self.locators.EMAIL_INPUT)
        element.clear()
        element.send_keys(email)

    @allure.step("Нажать кнопку восстановления")
    def click_restore_button(self) -> None:
        """Кликает на кнопку восстановления пароля"""
        self.click(self.locators.RESTORE_BUTTON)

    @allure.step("Проверить активность кнопки восстановления")
    def is_restore_button_active(self) -> bool:
        """Проверяет, активна ли кнопка восстановления"""
        try:
            self.wait_until_clickable(self.locators.RESTORE_BUTTON, timeout=3)
            return True
        except TimeoutException:
            return False
