# base_page.py

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
from typing import Tuple, Callable, Any, Union
from config import BASE_URL
from selenium.webdriver.common.by import By


Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site/"
        self.default_timeout = 15  # Секунды

    def _wait_until(self,
                   condition: Callable[[WebDriver], Any],
                   timeout: Union[int, float, None] = None,
                   message: str = "") -> Any:
        try:
            wait_timeout = float(timeout) if timeout is not None else self.default_timeout
            return WebDriverWait(self.driver, wait_timeout).until(condition, message)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid timeout value: {timeout}. Must be numeric.") from e

    def _wait(self, locator: Locator, timeout: Union[int, float, None] = None) -> WebElement:
        return self._wait_until(
            EC.visibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не найден"
        )

    def click_element(self, locator: Locator, timeout: Union[int, float, None] = None) -> None:
        element = self._wait(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_field(self, locator: Locator, text: str, timeout: Union[int, float, None] = None) -> None:
        field = self._wait(locator, timeout)
        field.clear()
        field.send_keys(text)

    def is_element_present(self, locator: Locator, timeout: Union[int, float, None] = None) -> bool:
        try:
            wait_timeout = float(timeout) if timeout is not None else 5
            WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator))
            return True
        except (ValueError, TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, locator, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, url_part: str, timeout: Union[int, float, None] = None) -> bool:
        return self._wait_until(
            EC.url_contains(url_part),
            timeout=timeout,
            message=f"URL не содержит '{url_part}'"
        )

    def wait_for_clickable(self, locator: Locator, timeout: Union[int, float, None] = None) -> WebElement:
        return self._wait_until(
            EC.element_to_be_clickable(locator),
            timeout=timeout,
            message=f"Элемент {locator} не стал кликабельным"
        )

    def scroll_to_element(self, locator: Locator):
        element = self._wait(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def build_url(self, path=""):
        base = BASE_URL.rstrip('/')
        path = str(path).lstrip('/')
        return f"{base}/{path}" if path else base

    def close_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Modal_modal__close_')]"))
            )
            close_btn.click()
            time.sleep(0.5)  # Даем время для закрытия
        except TimeoutException:
            pass
