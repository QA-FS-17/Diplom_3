# mane_page.py

from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.remote.webdriver import WebDriver


class MainPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = self.base_url

    def go_to_login_page(self):
        self.click_element(MainPageLocators.LOGIN_BUTTON)

    def go_to_personal_account(self):
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)

    def go_to_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    def go_to_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)

    def select_ingredient(self, ingredient_type):
        if ingredient_type == "bun":
            locator = MainPageLocators.INGREDIENT_BUN
        elif ingredient_type == "sauce":
            locator = MainPageLocators.INGREDIENT_SAUCE
        else:
            locator = MainPageLocators.INGREDIENT_MAIN

        self.click_element(locator)

    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)

    def make_order(self):
        self.click_element(MainPageLocators.MAKE_ORDER_BUTTON)

    def is_modal_visible(self):
        return self.is_element_present(MainPageLocators.MODAL)

    def get_order_number(self):
        element = self._wait(MainPageLocators.ORDER_NUMBER)
        return element.text

    def get_ingredient_counter(self, ingredient_type):
        if ingredient_type == "bun":
            locator = MainPageLocators.INGREDIENT_BUN
        elif ingredient_type == "sauce":
            locator = MainPageLocators.INGREDIENT_SAUCE
        else:
            locator = MainPageLocators.INGREDIENT_MAIN

        ingredient = self._wait(locator)
        counter = ingredient.find_element(*MainPageLocators.INGREDIENT_COUNTER)
        return int(counter.text) if counter.text else 0

    def make_order_successfully(self):
        """Добавляет ингредиенты и оформляет заказ, возвращает номер заказа"""
        self.select_ingredient("bun")
        self.select_ingredient("sauce")
        self.make_order()
        order_number = self.get_order_number()
        self.close_modal()
        return order_number