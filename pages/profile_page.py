# profile_page.py

from .base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators
from selenium.webdriver.remote.webdriver import WebDriver


class ProfilePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = self.base_url + "account/profile"

    def go_to_order_history(self):
        """Переход в раздел истории заказов"""
        self.click_element(ProfilePageLocators.ORDER_HISTORY_LINK)

    def get_first_order_number(self):
        order = self._wait(ProfilePageLocators.FIRST_ORDER_IN_HISTORY)
        return order.text.split('\n')[0]

    def logout(self):
        """Выход из аккаунта"""
        self.click_element(ProfilePageLocators.LOGOUT_BUTTON)
        self.wait_for_url_contains("/login")

    def is_profile_page(self):
        """Проверка, что находимся на странице профиля"""
        return self.wait_for_url_contains("/account/profile")