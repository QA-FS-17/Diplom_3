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
        self._verify_page_loaded()

    def _verify_page_loaded(self) -> None:
        """Внутренняя проверка загрузки страницы"""
        self.wait_until_visible(self.locators.PROFILE_FORM)
        self.url_should_contain("account/profile")

    @allure.step("Нажать на ссылку истории заказов")
    def click_order_history_link(self) -> None:
        """Кликает на ссылку истории заказов без ожидания раздела"""
        self.click(self.locators.ORDER_HISTORY_LINK)
        self.wait_until_url_contains("order-history")

    @allure.step("Выйти из аккаунта")
    def logout(self) -> None:
        """Выполняет выход из аккаунта."""
        self.click(self.locators.LOGOUT_BUTTON)
        self.wait_until_url_contains("login")

    @allure.step("Проверить видимость формы профиля")
    def is_profile_form_visible(self) -> bool:
        """Проверяет видимость формы профиля."""
        return self.is_visible(self.locators.PROFILE_FORM)

    @allure.step("Проверить видимость истории заказов")
    def is_order_history_visible(self) -> bool:
        """Проверяет видимость раздела истории заказов."""
        return self.is_visible(self.locators.ORDER_HISTORY_SECTION)