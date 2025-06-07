# helpers.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Union, Tuple
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

logger = logging.getLogger(__name__)


@allure.step("Перетаскивание элемента на целевой элемент")
def drag_and_drop(driver: WebDriver, source: WebElement, target: WebElement) -> None:
    try:
        driver.execute_script("""
        function simulateDragDrop(sourceNode, targetNode) {
            const dragStart = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            sourceNode.dispatchEvent(dragStart);

            const dragOver = new DragEvent('dragover', { bubbles: true });
            targetNode.dispatchEvent(dragOver);

            const drop = new DragEvent('drop', {
                bubbles: true,
                dataTransfer: dragStart.dataTransfer
            });
            targetNode.dispatchEvent(drop);
        }
        simulateDragDrop(arguments[0], arguments[1]);
        """, source, target)
    except (WebDriverException, StaleElementReferenceException) as e:
        logger.error(f"Ошибка при перетаскивании: {str(e)}")
        raise


@allure.step("Проверка наличия заказа в списке")
def is_order_in_list(order_numbers: List[Union[str, int]], order_number: Union[str, int]) -> bool:
    try:
        return str(order_number) in map(str, order_numbers)
    except (TypeError, ValueError) as e:
        logger.warning(f"Ошибка преобразования типа заказа: {str(e)}")
        return False


@allure.step("Ожидание появления текста в элементе")
def wait_for_text_in_element(
        driver: WebDriver,
        locator: Tuple[str, str],
        expected_text: str,
        timeout: int = 10
) -> bool:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, expected_text))
    except TimeoutException:
        logger.debug(f"Текст '{expected_text}' не появился в элементе {locator}")
        return False
    except NoSuchElementException as e:
        logger.warning(f"Элемент не найден: {str(e)}")
        return False

@allure.step("Зарегистрировать нового пользователя")
def register_new_user(driver: WebDriver, user_data: dict) -> None:
    register_page = RegisterPage(driver)
    register_page.open()
    register_page.register(
        user_data["name"],
        user_data["email"],
        user_data["password"]
    )

@allure.step("Авторизовать пользователя")
def login_user(driver: WebDriver, email: str, password: str) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(email, password)

@allure.step("Полная регистрация и авторизация")
def full_register_and_login(driver: WebDriver, user_data: dict) -> None:
    register_new_user(driver, user_data)
    login_user(driver, user_data["email"], user_data["password"])