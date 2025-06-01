# main_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                     TimeoutException,
                                     WebDriverException,
                                     ElementClickInterceptedException)
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from typing import Dict


class MainPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = MainPageLocators()
        self._base_url = "https://stellarburgers.nomoreparties.site"
        self._modal_timeout = 5

    @allure.step("Открыть главную страницу")
    def open(self) -> 'MainPage':
        """Открывает главную страницу и возвращает экземпляр MainPage"""
        try:
            self.driver.get(self._base_url)
            self._wait_until(
                lambda d: self._base_url == d.current_url,
                message="Не удалось загрузить главную страницу"
            )
            return self
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера: {str(e)}")

    @allure.step("Проверить видимость раздела ингредиентов")
    def is_ingredients_section_visible(self) -> bool:
        """Проверяет видимость раздела ингредиентов с ожиданием"""
        try:
            element = self._wait_until(
                EC.presence_of_element_located(self._locators.INGREDIENTS_SECTION),
                timeout=3
            )
            return self._is_visible(element)
        except (NoSuchElementException, TimeoutException):
            return False

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self) -> None:
        """Кликает на первый доступный ингредиент с проверкой"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.INGREDIENT_ITEM),
                message="Ингредиент не доступен для клика"
            )
            self._click(element)
        except TimeoutException as e:
            raise RuntimeError(f"Ингредиент не найден: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть: {str(e)}")

    @allure.step("Проверить состояние модального окна")
    def is_modal_visible(self) -> bool:
        """Проверяет видимость модального окна с ожиданием"""
        try:
            element = self._wait_until(
                EC.presence_of_element_located(self._locators.MODAL_WINDOW),
                timeout=self._modal_timeout
            )
            return self._is_visible(element)
        except (NoSuchElementException, TimeoutException):
            return False

    @allure.step("Закрыть модальное окно")
    def close_modal(self) -> None:
        """Закрывает модальное окно с проверкой"""
        try:
            if not self.is_modal_visible():
                return

            close_button = self._wait_until(
                EC.element_to_be_clickable(self._locators.MODAL_CLOSE_BUTTON),
                timeout=self._modal_timeout
            )
            self._click(close_button)
            self._wait_until(
                lambda d: not self.is_modal_visible(),
                timeout=self._modal_timeout,
                message="Модальное окно не закрылось"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка при закрытии: {str(e)}")

    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter(self) -> int:
        """Возвращает значение счетчика с обработкой ошибок"""
        try:
            element = self._wait_until(
                EC.presence_of_element_located(self._locators.INGREDIENT_COUNTER),
                timeout=2
            )
            return int(element.text) if element.text.isdigit() else 0
        except (NoSuchElementException, TimeoutException, ValueError):
            return 0

    @allure.step("Перейти в конструктор")
    def navigate_to_constructor(self) -> None:
        """Переходит в конструктор с проверкой"""
        try:
            button = self._wait_until(
                EC.element_to_be_clickable(self._locators.CONSTRUCTOR_BUTTON),
                message="Кнопка конструктора не доступна"
            )
            self._click(button)
            self._wait_until(
                lambda d: "stellarburgers" in d.current_url,
                message="Не удалось перейти в конструктор"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка навигации: {str(e)}")

    @allure.step("Перейти в ленту заказов")
    def navigate_to_order_feed(self) -> None:
        """Переходит в ленту заказов с проверкой"""
        try:
            button = self._wait_until(
                EC.element_to_be_clickable(self._locators.ORDER_FEED_BUTTON),
                message="Кнопка ленты заказов не доступна"
            )
            self._click(button)
            self._wait_until(
                lambda d: "feed" in d.current_url,
                message="Не удалось перейти в ленту заказов"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка навигации: {str(e)}")

    @allure.step("Оформить заказ")
    def make_order(self) -> str:
        """Оформляет заказ с ожиданием номера"""
        try:
            button = self._wait_until(
                EC.element_to_be_clickable(self._locators.MAKE_ORDER_BUTTON),
                message="Кнопка оформления не доступна"
            )
            self._click(button)

            order_element = self._wait_until(
                EC.visibility_of_element_located(self._locators.ORDER_NUMBER),
                timeout=15,
                message="Не дождались номера заказа"
            )
            return order_element.text
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут оформления: {str(e)}")

    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient_to_constructor(self) -> None:
        """Добавляет ингредиент через drag-and-drop"""
        try:
            ingredient = self._wait_until(
                EC.presence_of_element_located(self._locators.INGREDIENT_ITEM),
                message="Ингредиент не найден"
            )
            constructor = self._wait_until(
                EC.presence_of_element_located(self._locators.CONSTRUCTOR_AREA),
                message="Область конструктора не найдена"
            )
            self._drag_and_drop(ingredient, constructor)
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка добавления: {str(e)}")

    @allure.step("Проверить состояние страницы")
    def check_page_state(self) -> Dict[str, bool]:
        """Возвращает состояние страницы"""
        return {
            'url': self.driver.current_url,
            'constructor_visible': self._is_element_present(self._locators.CONSTRUCTOR_SECTION),
            'ingredients_visible': self.is_ingredients_section_visible()
        }

    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self) -> None:
        """Переходит в личный кабинет пользователя"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.PERSONAL_ACCOUNT_BUTTON),
                message="Кнопка 'Личный кабинет' не доступна"
            )
            self._click(element)
            self._wait_until(
                lambda d: "account/profile" in d.current_url,
                message="Не удалось перейти в личный кабинет"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка перехода в личный кабинет: {str(e)}")