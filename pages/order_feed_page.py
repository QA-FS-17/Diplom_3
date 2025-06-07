# order_feed_page.py

import allure
import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
from .base_page import BasePage
from locators.modal_locators import ModalLocators
from locators.order_feed_locators import OrderFeedLocators
from config import config


logger = logging.getLogger(__name__)


class OrderFeedPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, config.ORDER_FEED_URL)
        self.locators = OrderFeedLocators()
        self.modal_locators = ModalLocators()
        self.modal_timeout = 5

    @allure.step("Открыть ленту заказов")
    def open(self) -> None:
        """Открывает страницу ленты заказов и проверяет её загрузку."""
        super().open()
        self.wait_until_visible(self.locators.PAGE_HEADER)

    @allure.step("Получить номер первого заказа")
    def get_first_order_number(self) -> str:
        """Возвращает номер первого заказа в ленте."""
        return self.get_text(self.locators.FIRST_ORDER_NUMBER)

    @allure.step("Получить номер заказа из модального окна")
    def get_modal_order_number(self) -> str:
        """Возвращает номер заказа из модального окна."""
        return self.get_text(self.locators.MODAL_ORDER_NUMBER, timeout=self.modal_timeout)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self) -> bool:
        """Проверяет видимость модального окна с деталями заказа."""
        return self.is_visible(self.locators.ORDER_MODAL)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self) -> None:
        """Закрывает модальное окно с деталями заказа."""
        if self.is_order_modal_visible():
            self.click(self.modal_locators.MODAL_CLOSE_BUTTON)
            self.wait_until_not_visible(self.locators.ORDER_MODAL)

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        """Возвращает общее количество выполненных заказов."""
        count_text = self.get_text(self.locators.TOTAL_ORDERS_COUNT)
        return self._parse_count_text(count_text)

    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self) -> int:
        """Возвращает количество заказов за сегодня."""
        count_text = self.get_text(self.locators.TODAY_ORDERS_COUNT)
        return self._parse_count_text(count_text)

    @allure.step("Получить заказы в работе")
    def get_orders_in_progress(self) -> List[str]:
        """Возвращает номера заказов в работе."""
        elements = self._find_elements(self.locators.ORDERS_IN_PROGRESS)
        return [element.text for element in elements]

    @allure.step("Получить все номера заказов")
    def get_all_order_numbers(self) -> List[str]:
        """Возвращает список всех видимых номеров заказов."""
        elements = self._find_elements(self.locators.ORDER_ITEM)
        return [self._get_order_number(element) for element in elements]

    def _get_order_number(self, order_element: WebElement) -> str:
        """Извлекает номер заказа из элемента."""
        try:
            return order_element.find_element(*self.locators.ORDER_NUMBER).text
        except NoSuchElementException:
            return ""

    def _find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Находит элементы по локатору или возвращает пустой список."""
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            return []

    @staticmethod
    def _parse_count_text(count_text: str) -> int:
        """Преобразует текст счетчика в число."""
        try:
            return int(count_text)
        except ValueError as e:
            logger.error(f"Ошибка преобразования счетчика: {count_text}")
            raise ValueError(f"Некорректное значение счетчика: {count_text}") from e