# main_page.py

from allure import step
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()

    @step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.base_url)
        return self

    @step("Добавить ингредиент в конструктор")
    def add_ingredient(self, ingredient_type: str):
        section = {
            "bun": self.locators.BUN_SECTION,
            "sauce": self.locators.SAUCE_SECTION,
            "filling": self.locators.FILLING_SECTION
        }[ingredient_type]
        self.drag_and_drop(section, self.locators.CONSTRUCTOR_AREA)
        return self

    @step("Оформить заказ")
    def make_order(self):
        self.click(self.locators.ORDER_BUTTON)
        return self

    @step("Открыть детали ингредиента")
    def open_ingredient_details(self):
        self.click(self.locators.INGREDIENT_ITEM)
        return self

    @step("Закрыть модальное окно")
    def close_modal(self):
        self.click(self.locators.MODAL_CLOSE_BUTTON)
        return self

    @step("Перейти в личный кабинет")
    def go_to_profile(self):
        self.click(self.locators.PERSONAL_ACCOUNT_BUTTON)
        return self

    @step("Перейти в ленту заказов")
    def go_to_order_feed(self):
        self.click(self.locators.ORDER_FEED_BUTTON)
        return self