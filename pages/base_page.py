# base_page.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException
)
from typing import Tuple, Callable, Any, Union
import allure


class BasePage:
    """Абстрактный базовый класс для всех page objects"""

    def __init__(self, driver: WebDriver):
        """
        Инициализация базовой страницы
        :param driver: WebDriver instance
        """
        self.driver = driver
        self._timeout = 15

    @property
    def timeout(self) -> int:
        """Таймаут ожидания по умолчанию"""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        """Установка таймаута ожидания"""
        self._timeout = value

    def _wait_until(self,
                    condition: Callable[[WebDriver], Any],
                    timeout: Union[int, float, None] = None,
                    message: str = "") -> Any:
        """
        Абстрактное ожидание условия
        :param condition: Ожидаемое условие
        :param timeout: Время ожидания
        :param message: Сообщение об ошибке
        """
        try:
            wait_timeout = float(timeout) if timeout is not None else self.timeout
            return WebDriverWait(self.driver, wait_timeout).until(condition, message)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid timeout value: {timeout}") from e

    @allure.step("Клик по элементу")
    def _click(self, element: WebElement) -> None:
        """Абстрактный клик по элементу"""
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввод текста")
    def _type_text(self, element: WebElement, text: str) -> None:
        """Абстрактный ввод текста"""
        element.clear()
        element.send_keys(text)

    @allure.step("Проверка видимости элемента")
    def _is_visible(self, element: WebElement) -> bool:
        """Абстрактная проверка видимости элемента"""
        try:
            return element.is_displayed()
        except (NoSuchElementException, WebDriverException):
            return False

    @allure.step("Ожидание видимости элемента")
    def _wait_visibility(self, element: WebElement, timeout: Union[int, float, None] = None) -> WebElement:
        """Абстрактное ожидание видимости элемента"""
        return self._wait_until(
            lambda d: element.is_displayed(),
            timeout=timeout,
            message="Элемент не стал видимым"
        )

    @allure.step("Прокрутка к элементу")
    def _scroll_to(self, element: WebElement) -> None:
        """Абстрактная прокрутка к элементу"""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    @allure.step("Drag-and-drop элемента")
    def _drag_and_drop(self, source: WebElement, target: WebElement) -> None:
        """
        Абстрактная реализация drag-and-drop
        :param source: Элемент, который перетаскиваем
        :param target: Элемент, куда перетаскиваем
        """
        self.driver.execute_script("""
            function simulateDragDrop(sourceNode, targetNode) {
                const dragStartEvent = new DragEvent('dragstart', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: new DataTransfer()
                });
                sourceNode.dispatchEvent(dragStartEvent);

                const dropEvent = new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dragStartEvent.dataTransfer
                });
                targetNode.dispatchEvent(dropEvent);

                const dragEndEvent = new DragEvent('dragend', {
                    bubbles: true,
                    cancelable: true
                });
                sourceNode.dispatchEvent(dragEndEvent);
            }
            simulateDragDrop(arguments[0], arguments[1]);
        """, source, target)

    @allure.step("Проверка наличия элемента")
    def _is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Абстрактная проверка наличия элемента
        :param locator: Локатор элемента (кортеж из стратегии и значения)
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False