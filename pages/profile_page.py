# profile_page.py

from allure import step
from .base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ProfilePageLocators()

    @step("Открыть профиль")
    def open(self):
        self.driver.get(f"{self.base_url}/account/profile")
        return self

    @step("Перейти в историю заказов")
    def go_to_order_history(self):
        self.click(self.locators.ORDER_HISTORY_LINK)
        return self

    @step("Выйти из аккаунта")
    def logout(self):
        self.click(self.locators.LOGOUT_BUTTON)
        return self

    @step("Получить номер последнего заказа")
    def get_last_order_number(self) -> str:
        orders = self.driver.find_elements(*self.locators.ORDER_HISTORY_ITEM)
        return orders[0].find_element(*self.locators.ORDER_NUMBER).text