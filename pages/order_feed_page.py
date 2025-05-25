# order_feed_page.py

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site"
        self.locators = OrderFeedLocators()
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(f"{self.base_url}/feed")
        self.wait.until(
            EC.visibility_of_element_located(self.locators.ORDER_FEED_HEADER),
            "Заголовок ленты заказов не отображается"
        )

    def click_first_order(self):
        orders = self.wait.until(
            EC.presence_of_all_elements_located(OrderFeedLocators.ORDER_ITEMS)
        )
        first_order = orders[0]
        ActionChains(self.driver).move_to_element(first_order).click().perform()

    def is_order_modal_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(OrderFeedLocators.ORDER_MODAL)
        ).is_displayed()

    def get_order_numbers(self) -> list[str]:
        return [
            element.text for element in
            self.wait.until(
                EC.presence_of_all_elements_located(self.locators.ORDER_NUMBER_IN_LIST),
                "Не найдены номера заказов"
            )
        ]

    def is_order_in_list(self, order_number: str) -> bool:
        return str(order_number) in self.get_order_numbers()

    def get_total_orders_count(self) -> int:
        element = self.wait.until(
            EC.visibility_of_element_located(self.locators.TOTAL_ORDERS),
            "Элемент с общим количеством заказов не найден"
        )
        return int(element.text)

    def get_today_orders_count(self) -> int:
        element = self.wait.until(
            EC.visibility_of_element_located(self.locators.TODAY_ORDERS),
            "Элемент с количеством заказов за сегодня не найден"
        )
        return int(element.text)

    def is_order_in_progress(self, order_number: str) -> bool:
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.locators.IN_PROGRESS_ORDERS),
            "Не найдены заказы в работе"
        )
        return any(str(order_number) in element.text for element in elements)

    def get_order_modal_number(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.locators.MODAL_ORDER_NUMBER),
            "Номер заказа в модальном окне не отображается"
        ).text

    def get_first_order_number(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.locators.ORDER_NUMBER_IN_LIST),
            "Номер первого заказа не отображается"
        ).text

    def wait_for_order_in_progress(self, order_number: str, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(str(order_number) in order.text
                              for order in d.find_elements(*self.locators.IN_PROGRESS_ORDERS)),
                f"Заказ {order_number} не появился в разделе 'В работе'"
            )
            return True
        except TimeoutException:
            return False
