# order_feed_page.py

from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from selenium.webdriver.remote.webdriver import WebDriver


class OrderFeedPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = self.base_url + "feed"

    def open_order_details(self):
        self.click_element(OrderFeedLocators.ORDER_ITEM)

    def close_order_details(self):
        self.click_element(OrderFeedLocators.ORDER_MODAL_CLOSE)

    def is_order_modal_visible(self):
        return self.is_element_present(OrderFeedLocators.ORDER_MODAL)

    def get_total_orders_count(self):
        element = self._wait(OrderFeedLocators.TOTAL_ORDERS_COUNT)
        return int(element.text)

    def get_today_orders_count(self):
        element = self._wait(OrderFeedLocators.TODAY_ORDERS_COUNT)
        return int(element.text)

    def get_in_progress_orders(self):
        elements = self.driver.find_elements(*OrderFeedLocators.IN_PROGRESS_ORDERS)
        return [element.text for element in elements]

    def get_first_order_number(self):
        element = self._wait(OrderFeedLocators.ORDER_ITEM)
        return element.text.split('\n')[0]

    def get_order_number_in_progress(self):
        element = self._wait(OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS)
        return element.text