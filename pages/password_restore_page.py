# password_restore_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (NoSuchElementException,
                                      TimeoutException,
                                      WebDriverException,
                                      ElementClickInterceptedException,
                                      ElementNotInteractableException)
from .base_page import BasePage
from locators.password_restore_locators import PasswordRestoreLocators
from typing import Tuple, Optional


class PasswordRestorePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = PasswordRestoreLocators()
        self._page_path = "forgot-password"

    @property
    def _base_url(self) -> str:
        return "https://stellarburgers.nomoreparties.site"

    @allure.step("Открыть страницу восстановления пароля")
    def open(self) -> 'PasswordRestorePage':
        """Открывает страницу восстановления пароля"""
        try:
            self.driver.get(f"{self._base_url}/{self._page_path}")
            self._wait_until(lambda d: self._page_path in d.current_url)
            return self
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера при открытии страницы: {str(e)}")

    @allure.step("Проверить видимость формы восстановления")
    def is_restore_form_visible(self) -> bool:
        """Проверяет видимость формы восстановления пароля"""
        try:
            element = self.driver.find_element(*self._locators.RESTORE_FORM)
            return self._is_visible(element)
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False

    @allure.step("Восстановить пароль для email {email}")
    def restore_password(self, email: str) -> None:
        """Заполняет email и нажимает кнопку восстановления"""
        try:
            email_input = self.driver.find_element(*self._locators.EMAIL_INPUT)
            self._type_text(email_input, email)
            restore_button = self.driver.find_element(*self._locators.RESTORE_BUTTON)
            self._click(restore_button)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти элемент формы: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на кнопку: {str(e)}")
        except ElementNotInteractableException as e:
            raise RuntimeError(f"Элемент не доступен для взаимодействия: {str(e)}")

    @allure.step("Переключить видимость пароля")
    def toggle_password_visibility(self) -> None:
        """Переключает видимость введенного пароля"""
        try:
            show_button = self.driver.find_element(*self._locators.SHOW_PASSWORD_BUTTON)
            self._click(show_button)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти кнопку показа пароля: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на кнопку: {str(e)}")
        except ElementNotInteractableException as e:
            raise RuntimeError(f"Кнопка не доступна для взаимодействия: {str(e)}")

    @allure.step("Проверить подсветку поля пароля")
    def is_password_field_highlighted(self) -> bool:
        """Проверяет подсветку поля ввода пароля"""
        try:
            password_input = self.driver.find_element(*self._locators.PASSWORD_INPUT)
            class_attr = password_input.get_attribute("class")
            return "input_status_active" in class_attr if class_attr else False
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти поле ввода пароля: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при ожидании поля ввода: {str(e)}")

    @allure.step("Получить атрибут элемента")
    def get_element_attribute(self, locator: Tuple[str, str], attribute: str) -> Optional[str]:
        """Возвращает значение атрибута элемента"""
        try:
            element = self._wait_until(
                lambda d: d.find_element(*locator),
                message=f"Элемент с локатором {locator} не найден"
            )
            return element.get_attribute(attribute)
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при ожидании элемента: {str(e)}")
        except NoSuchElementException as e:
            raise RuntimeError(f"Элемент не найден: {str(e)}")