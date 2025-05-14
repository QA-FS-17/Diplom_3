# base_page.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException
)
from typing import Tuple

Locator = Tuple[str, str]

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site/"
        self.default_timeout = 15

    def _wait_until(self, condition, timeout=None, message=""):
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(condition, message)

    def _wait(self, locator: Locator, timeout=None) -> WebElement:
        return self._wait_until(
            EC.visibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не найден"
        )

    def click_element(self, locator: Locator, timeout=None) -> None:
        element = self._wait(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_field(self, locator: Locator, text: str, timeout=None) -> None:
        field = self._wait(locator, timeout)
        field.clear()
        field.send_keys(text)

    def is_element_present(self, locator: Locator, timeout=None) -> bool:
        try:
            return self._wait(locator, timeout or 5).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
        except StaleElementReferenceException:
            try:
                return self.driver.find_element(*locator).is_displayed()
            except (NoSuchElementException, StaleElementReferenceException):
                return False

    def wait_for_url_contains(self, url_part: str, timeout=None) -> bool:
        return self._wait_until(
            EC.url_contains(url_part),
            timeout=timeout,
            message=f"URL не содержит '{url_part}'"
        )