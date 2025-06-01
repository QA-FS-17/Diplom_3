# register_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        WebDriverException,
                                        ElementClickInterceptedException)
from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators


class RegisterPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = RegisterPageLocators()
        self._page_path = "register"

    @property
    def _base_url(self) -> str:
        return "https://stellarburgers.nomoreparties.site"

    @allure.step("Открыть страницу регистрации")
    def open(self) -> 'RegisterPage':
        """Открывает страницу регистрации пользователя"""
        try:
            self.driver.get(f"{self._base_url}/{self._page_path}")
            self._wait_until(lambda d: self._page_path in d.current_url)
            return self
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы регистрации: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера при открытии страницы регистрации: {str(e)}")

    @allure.step("Зарегистрировать пользователя с именем {name}, email {email} и паролем {password}")
    def register(self, name: str, email: str, password: str) -> None:
        """Выполняет регистрацию нового пользователя"""
        try:
            name_input = self.driver.find_element(*self._locators.NAME_INPUT)
            self._type_text(name_input, name)

            email_input = self.driver.find_element(*self._locators.EMAIL_INPUT)
            self._type_text(email_input, email)

            password_input = self.driver.find_element(*self._locators.PASSWORD_INPUT)
            self._type_text(password_input, password)

            register_button = self.driver.find_element(*self._locators.REGISTER_BUTTON)
            self._click(register_button)

            self._wait_until(lambda d: "login" in d.current_url)

        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти элемент формы регистрации: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на кнопку регистрации: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при регистрации пользователя: {str(e)}")

    @allure.step("Проверить наличие сообщения об ошибке")
    def should_have_error_message(self, expected_message: str) -> bool:
        """Проверяет наличие ожидаемого сообщения об ошибке"""
        try:
            error_element = self._wait_until(
                lambda d: d.find_element(*self._locators.ERROR_MESSAGE),
                message="Сообщение об ошибке не найдено"
            )
            actual_message = error_element.text
            return expected_message in actual_message
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    @allure.step("Перейти на страницу входа")
    def go_to_login_page(self) -> None:
        """Переходит на страницу входа в систему"""
        try:
            login_link = self.driver.find_element(*self._locators.LOGIN_LINK)
            self._click(login_link)
            self._wait_until(lambda d: "login" in d.current_url)
        except NoSuchElementException as e:
            raise RuntimeError(f"Не удалось найти ссылку на страницу входа: {str(e)}")
        except ElementClickInterceptedException as e:
            raise RuntimeError(f"Не удалось кликнуть на ссылку входа: {str(e)}")
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при переходе на страницу входа: {str(e)}")