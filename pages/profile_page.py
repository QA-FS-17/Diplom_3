# profile_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (NoSuchElementException,
                                     TimeoutException,
                                     WebDriverException,
                                     ElementClickInterceptedException)
from .base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators


class ProfilePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = ProfilePageLocators()
        self._page_path = "account/profile"

    @property
    def _base_url(self) -> str:
        return "https://stellarburgers.nomoreparties.site"

    @allure.step("Открыть страницу профиля")
    def open(self) -> 'ProfilePage':
        """Открывает страницу профиля пользователя"""
        try:
            self.driver.get(f"{self._base_url}/{self._page_path}")
            self._wait_until(lambda d: self._page_path in d.current_url)
            return self
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы профиля: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера при открытии страницы профиля: {str(e)}")

    @allure.step("Проверить видимость формы профиля")
    def is_profile_form_visible(self) -> bool:
        """Проверяет видимость формы профиля пользователя"""
        try:
            element = self.driver.find_element(*self._locators.PROFILE_FORM)
            return self._is_visible(element)
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False

    @allure.step("Перейти в историю заказов")
    def go_to_order_history(self) -> None:
        """Переходит на страницу истории заказов"""
        try:
            order_history_link = self.driver.find_element(*self._locators.ORDER_HISTORY_LINK)
            self._click(order_history_link)
            self._wait_until(lambda d: "order-history" in d.current_url)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти ссылку на историю заказов: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на ссылку истории заказов: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при переходе в историю заказов: {str(e)}")

    @allure.step("Выйти из аккаунта")
    def logout(self) -> None:
        """Выполняет выход из аккаунта пользователя"""
        try:
            logout_button = self.driver.find_element(*self._locators.LOGOUT_BUTTON)
            self._click(logout_button)
            self._wait_until(lambda d: "login" in d.current_url)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти кнопку выхода: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на кнопку выхода: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при выходе из аккаунта: {str(e)}")

    @allure.step("Проверить, что пользователь вышел")
    def is_logged_out(self) -> bool:
        """Проверяет, выполнен ли выход из аккаунта"""
        try:
            return "login" in self.driver.current_url
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка при проверке URL: {str(e)}")