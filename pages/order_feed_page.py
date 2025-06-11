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
from helpers import CounterNotIncreasedError
from config import config

logger = logging.getLogger(__name__)


class OrderFeedPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.locators = OrderFeedLocators()
        self.modal_locators = ModalLocators()
        self.modal_timeout = 5

    @allure.step("Открыть ленту заказов")
    def open(self) -> None:
        """Открывает страницу ленты заказов и проверяет её загрузку."""
        self.url = config.ORDER_FEED_URL
        self.logger.info(f"Открытие OrderFeedPage, URL: {self.url}")
        super().open()
        self.wait_until_visible(self.locators.PAGE_HEADER)

    @allure.step("Кликнуть на первый заказ в ленте")
    def click_first_order(self) -> None:
        """Кликает на первый заказ в ленте заказов"""
        self.click(self.locators.FIRST_ORDER_NUMBER)
        self.wait_until_visible(self.locators.ORDER_MODAL)

    @allure.step("Получить номер первого заказа")
    def get_first_order_number(self) -> str:
        """Возвращает номер первого заказа в ленте."""
        return self.get_text(self.locators.FIRST_ORDER_NUMBER)

    @allure.step("Получить номер заказа из модального окна")
    def get_modal_order_number(self) -> str:
        """Возвращает номер заказа из модального окна."""
        return self.get_text(self.locators.MODAL_ORDER_NUMBER, timeout=10)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self) -> bool:
        """Проверяет видимость модального окна с деталями заказа."""
        return self.is_visible(self.locators.ORDER_MODAL)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self) -> None:
        """Закрывает модальное окно с деталями заказа."""
        if self.is_order_modal_visible():
            self.click(self.modal_locators.MODAL_CLOSE_BUTTON)
            self.wait_until_not_visible(self.locators.ORDER_MODAL, timeout=10)

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

    @allure.step("Извлекает номер заказа из элемента")
    def _get_order_number(self, order_element: WebElement) -> str:
        """Извлекает номер заказа из элемента."""
        try:
            return order_element.find_element(*self.locators.ORDER_NUMBER).text
        except NoSuchElementException:
            return ""

    @allure.step("Находит элементы по локатору или возвращает пустой список")
    def _find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Находит элементы по локатору или возвращает пустой список."""
        try:
            return super().find_elements(*locator)
        except NoSuchElementException:
            return []

    @staticmethod
    @allure.step("Преобразует текст счетчика в число")
    def _parse_count_text(count_text: str) -> int:
        """Преобразует текст счетчика в число."""
        try:
            return int(count_text)
        except ValueError as e:
            logger.error(f"Ошибка преобразования счетчика: {count_text}")
            raise ValueError(f"Некорректное значение счетчика: {count_text}") from e

    @allure.step("Проверяет видимость заголовка страницы 'Лента заказов'")
    def is_page_header_visible(self) -> bool:
        """Проверяет видимость заголовка страницы 'Лента заказов'."""
        return self.is_visible(self.locators.PAGE_HEADER)

    @allure.step("Получить текущий URL")
    def get_current_page_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.get_current_url()

    @allure.step("Получить заказы в работе")
    def get_orders_in_progress(self) -> List[str]:
        """Возвращает номера заказов в работе."""
        elements = self._find_elements(self.locators.ORDERS_IN_PROGRESS)
        orders = []
        for element in elements:
            text = element.text.strip()
            # Пропускаем служебные сообщения
            if text.lower().startswith("все текущие заказы готовы"):
                continue
            if text.startswith("#"):
                text = text[1:]
            if text.isdigit():
                orders.append(text)
        return orders

    def wait_for_order_in_progress(self, order_number, timeout=15):
        """Ожидает, что заказ появится в списке заказов "В работе"."""
        def order_appeared():
            return order_number in self.get_orders_in_progress()

        self.wait_for_condition(order_appeared, timeout=timeout,
                                message=f"Заказ {order_number} не появился в 'В работе'")

    @allure.step("Проверить загрузку страницы ленты заказов")
    def _verify_page_loaded(self) -> None:
        """Проверяет, что страница ленты заказов загружена."""
        self.wait_until_visible(self.locators.PAGE_HEADER)

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        """Получает значение счетчика через безопасный метод"""
        return self.get_numeric_value(self.locators.TOTAL_ORDERS_COUNT)

    @allure.step("Ожидание увеличения счетчика")
    def wait_for_total_increase(self, initial_value: int, timeout: int = 20) -> bool:
        """Ожидает увеличения значения счетчика"""

        def is_increased() -> bool:
            try:
                return self.get_total_orders_count() > initial_value
            except ValueError:
                return False

        return self.wait_for_condition(
            is_increased,
            timeout=timeout,
            message=f"Счетчик не превысил {initial_value} за {timeout} сек"
        )

    @allure.step("Получить валидированное значение счетчика")
    def get_validated_counter_value(self) -> int:
        self.open()
        count = self.get_total_orders_count()

        if not isinstance(count, int) or count < 0:
            raise ValueError(f"Некорректное значение счетчика: {count}")

        self.logger.info(f"Начальное значение счетчика: {count}")
        return count

    @allure.step("Проверить увеличение счетчика")
    def verify_counter_increase(self, initial_value: int) -> None:
        current = self.get_total_orders_count()
        if current <= initial_value:
            raise CounterNotIncreasedError(initial_value, current)
        self.logger.info(f"Счетчик увеличился: {initial_value} → {current}")