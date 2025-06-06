# base_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from typing import Tuple, Any, Callable, Optional
from config import config

logger = logging.getLogger(__name__)


class BasePage:
    """Базовый класс для всех Page Object, реализующий основные методы взаимодействия с веб-страницей."""

    def __init__(self, driver: WebDriver, url_suffix: str = ""):
        """
        Инициализация базовой страницы.

        Args:
            driver: Экземпляр WebDriver
            url_suffix: Суффикс URL для конкретной страницы
        """
        self.driver = driver
        self.base_url = f"{config.BASE_URL}/{url_suffix.lstrip('/')}"
        self.default_timeout = config.DEFAULT_TIMEOUT

    @property
    def wait(self) -> WebDriverWait:
        """Возвращает экземпляр WebDriverWait с default_timeout"""
        return WebDriverWait(self.driver, self.default_timeout)

    # ==================== Основные методы взаимодействия ====================

    @allure.step("Открыть страницу")
    def open(self) -> None:
        """Открывает страницу и проверяет её загрузку."""
        self.driver.get(self.base_url)
        self.wait_for_page_loaded()
        self._verify_page_loaded()

    @allure.step("Клик по элементу {locator}")
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Кликает по элементу с ожиданием его кликабельности.

        Args:
            locator: Локатор элемента (By, value)
            timeout: Время ожидания в секундах
        """
        element = self.wait_until_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self._click_via_js(element)

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def type_text(self, locator: Tuple[str, str], text: str, clear: bool = True) -> None:
        """
        Вводит текст в элемент.

        Args:
            locator: Локатор элемента
            text: Текст для ввода
            clear: Нужно ли очищать поле перед вводом
        """
        element = self.wait_until_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    # ==================== Методы получения данных ====================

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Возвращает текст элемента.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        element = self.wait_until_visible(locator, timeout)
        return element.text.strip()

    @allure.step("Получить атрибут элемента")
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Возвращает значение атрибута элемента.

        Args:
            locator: Локатор элемента
            attribute: Название атрибута
        """
        try:
            element = self.wait_until_present(locator)
            return element.get_attribute(attribute) or ""
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Не удалось получить атрибут: {str(e)}")
            raise

    # ==================== Методы ожидания ====================

    @allure.step("Ожидание выполнения условия")
    def wait_for_condition(self, condition: Callable[[], bool],
                           timeout: Optional[int] = None,
                           message: str = "") -> bool:
        """
        Ожидает выполнения произвольного условия.

        Args:
            condition: Функция-условие, возвращающая bool
            timeout: Время ожидания в секундах
            message: Сообщение об ошибке

        Returns:
            True если условие выполнено
        """
        wait_timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                lambda _: condition(),
                message=message or f"Условие не выполнено за {wait_timeout} секунд"
            )
        except TimeoutException as e:
            logger.error(f"Timeout waiting for condition: {str(e)}")
            raise

    @allure.step("Ожидание присутствия элемента в DOM")
    def wait_until_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает появления элемента в DOM (без проверки видимости).

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах

        Returns:
            Найденный WebElement
        """
        return self._wait_until(
            EC.presence_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не найден в DOM"
        )

    @allure.step("Ожидание видимости элемента {locator}")
    def wait_until_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает появления элемента в DOM и его видимости.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        return self._wait_until(
            EC.visibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не стал видимым"
        )

    @allure.step("Ожидание кликабельности элемента {locator}")
    def wait_until_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает, пока элемент станет кликабельным.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        return self._wait_until(
            EC.element_to_be_clickable(locator),
            timeout=timeout,
            message=f"Элемент {locator} не стал кликабельным"
        )

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_loaded(self, timeout: Optional[int] = None) -> None:
        """
        Ожидает полной загрузки страницы.

        Args:
            timeout: Время ожидания в секундах
        """
        wait_timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException as e:
            logger.error(f"Страница не загрузилась за {wait_timeout} секунд")
            raise

    @allure.step("Ожидание URL содержащего '{expected_part}'")
    def wait_until_url_contains(self, expected_part: str, timeout: Optional[int] = None) -> bool:
        """
        Ожидает, пока URL будет содержать указанную строку.

        Args:
            expected_part: Часть URL для проверки
            timeout: Время ожидания в секундах
        """
        return self._wait_until(
            EC.url_contains(expected_part),
            timeout=timeout,
            message=f"URL не содержит '{expected_part}'"
        )

    @allure.step("Ожидание исчезновения элемента")
    def wait_until_not_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Ожидает, пока элемент перестанет быть видимым.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        return self._wait_until(
            EC.invisibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не исчез"
        )

    @allure.step("Ожидание появления текста в элементе")
    def wait_until_text_present(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> bool:
        """
        Ожидает появления текста в элементе.

        Args:
            locator: Локатор элемента
            text: Ожидаемый текст
            timeout: Время ожидания в секундах
        """
        return self._wait_until(
            EC.text_to_be_present_in_element(locator, text),
            timeout=timeout,
            message=f"Текст '{text}' не появился в элементе {locator}"
        )

    @allure.step("Проверка что URL содержит '{expected_part}'")
    def url_should_contain(self, expected_part: str) -> None:
        """
        Проверяет что текущий URL содержит указанную строку.
        Вызывает AssertionError если условие не выполняется.

        Args:
            expected_part: Часть URL для проверки
        """
        current_url = self.get_current_url()
        if expected_part.lower() not in current_url.lower():
            raise AssertionError(f"URL '{current_url}' не содержит '{expected_part}'")

    # ==================== Проверки состояния ====================

    @allure.step("Проверка видимости элемента {locator}")
    def is_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Проверяет видимость элемента.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        try:
            return self.wait_until_visible(locator, timeout) is not None
        except TimeoutException:
            return False

    @allure.step("Проверка присутствия элемента {locator}")
    def is_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Проверяет наличие элемента в DOM.

        Args:
            locator: Локатор элемента
            timeout: Время ожидания в секундах
        """
        try:
            self.wait_until_present(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ==================== Внутренние методы ====================

    def _wait_until(self, condition: Callable[[WebDriver], Any],
                    timeout: Optional[int] = None,
                    message: str = "") -> Any:
        """
        Базовый метод для ожидания условий.

        Args:
            condition: Условие для ожидания
            timeout: Время ожидания в секундах
            message: Сообщение об ошибке
        """
        wait_timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                condition,
                message=message
            )
        except TimeoutException as e:
            logger.error(f"Timeout waiting for condition: {message}")
            raise
        except WebDriverException as e:
            logger.error(f"WebDriver error while waiting: {str(e)}")
            raise

    @allure.step("Клик через JavaScript")
    def _click_via_js(self, element: WebElement) -> None:
        """Выполняет клик через JavaScript."""
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except WebDriverException as e:
            logger.error(f"JavaScript click failed: {str(e)}")
            raise

    def _verify_page_loaded(self) -> None:
        """Абстрактный метод для проверки загрузки страницы (должен быть реализован в дочерних классах)."""
        raise NotImplementedError("Метод должен быть реализован в дочернем классе")

    @allure.step("Выполнение перетаскивания через JavaScript")
    def _execute_drag_and_drop_js(self, source: WebElement, target: WebElement) -> None:
        """Внутренний метод для выполнения drag-and-drop через JS."""
        script = """
        function simulateDragDrop(sourceNode, targetNode) {
            // Создаем и инициируем событие dragstart
            const dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            sourceNode.dispatchEvent(dragStartEvent);

            // Создаем и инициируем событие dragover
            const dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            targetNode.dispatchEvent(dragOverEvent);

            // Создаем и инициируем событие drop
            const dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            targetNode.dispatchEvent(dropEvent);

            // Завершаем процесс событием dragend
            const dragEndEvent = new DragEvent('dragend', {
                bubbles: true,
                cancelable: true
            });
            sourceNode.dispatchEvent(dragEndEvent);
        }
        simulateDragDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(script, source, target)

    @allure.step("Прокрутка к элементу")
    def _scroll_to_element(self, element: WebElement) -> None:
        """Прокручивает страницу к указанному элементу."""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                element
            )
        except WebDriverException as e:
            logger.warning(f"Не удалось прокрутить к элементу: {str(e)}")