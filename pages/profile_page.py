# profile_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators
from config import config

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, config.PROFILE_URL)
        self.locators = ProfilePageLocators()

    @allure.step("Открыть страницу профиля")
    def open(self) -> None:
        """Открывает страницу профиля и проверяет её загрузку."""
        super().open()
        self.wait_until_visible(self.locators.PROFILE_FORM)

    @allure.step("Проверить видимость формы профиля")
    def is_profile_form_visible(self) -> bool:
        """Проверяет видимость формы профиля."""
        return self.is_visible(self.locators.PROFILE_FORM)

    @allure.step("Перейти в историю заказов")
    def go_to_order_history(self) -> None:
        """Переходит на страницу истории заказов."""
        self.click(self.locators.ORDER_HISTORY_LINK)
        self.wait_until_url_contains("order-history")

    @allure.step("Выйти из аккаунта")
    def logout(self) -> None:
        """Выполняет выход из аккаунта."""
        self.click(self.locators.LOGOUT_BUTTON)
        self.wait_until_url_contains("login")

    @allure.step("Проверить, что пользователь вышел")
    def is_logged_out(self) -> bool:
        """Проверяет, выполнен ли выход из аккаунта."""
        try:
            self.url_should_contain("login")
            return True
        except AssertionError:
            return False