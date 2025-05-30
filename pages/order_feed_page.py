# order_feed_page.py

from allure import step
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators

class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderFeedLocators()

    @step("Открыть ленту заказов")
    def open(self):
        self.driver.get(f"{self.base_url}/feed")
        return self

    @step("Открыть детали заказа")
    def open_order_details(self, order_index: int = 0):
        orders = self.driver.find_elements(*self.locators.ORDER_ITEM)
        orders[order_index].click()
        return self

    @step("Получить номер заказа")
    def get_order_number(self, order_index: int = 0) -> str:
        orders = self.driver.find_elements(*self.locators.ORDER_NUMBER)
        return orders[order_index].text

    @step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        return int(self._wait_element(self.locators.TOTAL_ORDERS).text)

    @step("Получить количество заказов за сегодня")
    def get_today_orders_count(self) -> int:
        return int(self._wait_element(self.locators.TODAY_ORDERS).text)