# order_feed_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        WebDriverException,
                                        ElementClickInterceptedException)
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from typing import List, Tuple


class OrderFeedPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = OrderFeedLocators()
        self._page_path = "feed"
        self._modal_timeout = 5  # Таймаут для модальных окон

    @property
    def _base_url(self) -> str:
        return "https://stellarburgers.nomoreparties.site"

    @allure.step("Открыть ленту заказов")
    def open(self) -> None:
        """Открывает страницу ленты заказов с проверкой загрузки"""
        try:
            self.driver.get(f"{self._base_url}/{self._page_path}")
            header = self._locators.PAGE_HEADER
            self._wait_until(
                EC.visibility_of_element_located(header),
                message="Заголовок страницы не отобразился"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера при открытии страницы: {str(e)}")

    @allure.step("Получить номер первого заказа")
    def get_first_order_number(self) -> str:
        """Возвращает номер первого заказа в ленте с ожиданием"""
        try:
            element = self._wait_until(
                EC.visibility_of_element_located(self._locators.FIRST_ORDER_NUMBER),
                message="Не дождались отображения номера заказа"
            )
            return element.text
        except TimeoutException as e:
            raise RuntimeError(f"Не удалось найти номер заказа: {str(e)}")

    @allure.step("Кликнуть на заказ {order_number}")
    def click_order(self, order_number: str) -> None:
        """Кликает на заказ с указанным номером с проверкой"""
        try:
            locator = self._format_locator(
                self._locators.ORDER_BY_NUMBER_TEMPLATE,
                order_number
            )
            element = self._wait_until(
                EC.element_to_be_clickable(locator),
                message=f"Заказ {order_number} не доступен для клика"
            )
            self._click(element)
        except TimeoutException as e:
            raise RuntimeError(f"Заказ {order_number} не найден: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на заказ: {str(e)}")

    @allure.step("Проверить видимость модального окна")
    def is_order_modal_visible(self) -> bool:
        """Проверяет видимость модального окна заказа с ожиданием"""
        try:
            element = self._wait_until(
                EC.presence_of_element_located(self._locators.ORDER_MODAL),
                timeout=self._modal_timeout
            )
            return self._is_visible(element)
        except (NoSuchElementException, TimeoutException):
            return False

    @allure.step("Получить номер заказа из модального окна")
    def get_modal_order_number(self) -> str:
        """Возвращает номер заказа из модального окна с ожиданием"""
        try:
            element = self._wait_until(
                EC.visibility_of_element_located(self._locators.MODAL_ORDER_NUMBER),
                timeout=self._modal_timeout,
                message="Не дождались отображения номера в модальном окне"
            )
            return element.text
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при ожидании модального окна: {str(e)}")

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self) -> None:
        """Закрывает модальное окно с проверкой успешного закрытия"""
        try:
            if not self.is_order_modal_visible():
                return

            close_button = self._wait_until(
                EC.element_to_be_clickable(self._locators.MODAL_CLOSE_BUTTON),
                timeout=self._modal_timeout
            )
            self._click(close_button)

            self._wait_until(
                lambda d: not self.is_order_modal_visible(),
                timeout=self._modal_timeout,
                message="Модальное окно не закрылось"
            )
        except NoSuchElementException as e:
            raise RuntimeError(f"Кнопка закрытия не найдена: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Модальное окно не закрылось: {str(e)}")

    @allure.step("Получить все номера заказов")
    def get_all_order_numbers(self) -> List[str]:
        """Возвращает список всех видимых номеров заказов с ожиданием"""
        try:
            self._wait_until(
                EC.presence_of_all_elements_located(self._locators.ALL_ORDER_NUMBERS),
                message="Не найдены номера заказов"
            )
            elements = self.driver.find_elements(*self._locators.ALL_ORDER_NUMBERS)
            return [element.text for element in elements]
        except TimeoutException:
            return []

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        """Возвращает общее количество выполненных заказов с проверкой"""
        try:
            element = self._wait_until(
                EC.visibility_of_element_located(self._locators.TOTAL_ORDERS_COUNT),
                message="Не дождались отображения счетчика заказов"
            )
            return int(element.text)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти счетчик заказов: {str(e)}")
        except ValueError as e:
            raise RuntimeError(f"Некорректное значение счетчика: {str(e)}")

    @allure.step("Проверить заказы в работе")
    def get_orders_in_progress(self) -> List[str]:
        """Возвращает номера заказов в работе с ожиданием"""
        try:
            self._wait_until(
                EC.presence_of_all_elements_located(self._locators.ORDERS_IN_PROGRESS),
                message="Не найдены заказы в работе"
            )
            elements = self.driver.find_elements(*self._locators.ORDERS_IN_PROGRESS)
            return [element.text for element in elements]
        except TimeoutException:
            return []

    @staticmethod
    def _format_locator(locator: Tuple[str, str], *values: str) -> Tuple[str, str]:
        """Форматирует локатор с динамическими значениями"""
        return locator[0], locator[1].format(*values)