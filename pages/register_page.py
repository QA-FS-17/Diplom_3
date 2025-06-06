# register_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators
from config import config

logger = logging.getLogger(__name__)


class RegisterPage(BasePage):
    """Page Object для страницы регистрации пользователя."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver, config.REGISTER_URL)
        self.locators = RegisterPageLocators()

    @allure.step("Открыть страницу регистрации")
    def open(self) -> None:
        """Открывает страницу регистрации и проверяет её загрузку."""
        super().open()
        self.wait_until_visible(self.locators.REGISTER_FORM)

    @allure.step("Зарегистрировать пользователя")
    def register(self, name: str, email: str, password: str) -> None:
        self.type_text(self.locators.NAME_INPUT, name)
        self.type_text(self.locators.EMAIL_INPUT, email)
        self.type_text(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.REGISTER_BUTTON)
        self.wait_until_url_contains("login")

    @allure.step("Проверить сообщение об ошибке")
    def is_error_message_displayed(self, expected_message: str) -> bool:
        try:
            error_text = self.get_text(self.locators.ERROR_MESSAGE)
            return expected_message in error_text
        except NoSuchElementException:
            logger.debug("Элемент с сообщением об ошибке не найден")
            return False
        except TimeoutException:
            logger.debug("Таймаут при ожидании сообщения об ошибке")
            return False

    @allure.step("Перейти на страницу входа")
    def go_to_login_page(self) -> None:
        """Переходит на страницу входа в систему."""
        self.click(self.locators.LOGIN_LINK)
        self.wait_until_url_contains("login")