# base_page.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple
import allure

Locator = Tuple[str, str]

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site"
        self.default_timeout = 10

    @allure.step("Ожидать элемент {locator}")
    def _wait_element(self, locator: Locator, timeout: int = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент {locator} не найден"
        )

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: Locator, timeout: int = None) -> None:
        element = self._wait_element(locator, timeout)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def fill(self, locator: Locator, text: str, timeout: int = None) -> None:
        element = self._wait_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Проверка видимости элемента {locator}")
    def is_visible(self, locator: Locator, timeout: int = None) -> bool:
        try:
            return self._wait_element(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверка URL на содержание '{url_part}'")
    def url_contains(self, url_part: str, timeout: int = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or self.default_timeout).until(
                EC.url_contains(url_part))
            return True
        except TimeoutException:
            return False

    @allure.step("Перетаскивание элемента {source} на {target}")
    def drag_and_drop(self, source: Locator, target: Locator):
        source_element = self._wait_element(source)
        target_element = self._wait_element(target)
        self.driver.execute_script("""
            const dataTransfer = new DataTransfer();
            const dragStart = new DragEvent('dragstart', { bubbles: true, dataTransfer });
            arguments[0].dispatchEvent(dragStart);
            const drop = new DragEvent('drop', { bubbles: true, dataTransfer });
            arguments[1].dispatchEvent(drop);
        """, source_element, target_element)