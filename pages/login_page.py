# login_page.py

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                     TimeoutException,
                                     WebDriverException,
                                     ElementClickInterceptedException)
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._locators = LoginPageLocators()
        self._page_path = "login"
        self._auth_timeout = 10

    @property
    def _base_url(self) -> str:
        return "https://stellarburgers.nomoreparties.site"

    @allure.step("Открытие страницы логина")
    def open(self) -> None:
        """Открывает страницу логина с проверкой загрузки"""
        try:
            self.driver.get(f"{self._base_url}/{self._page_path}")
            self._verify_page_loaded()
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут при загрузке страницы: {str(e)}")
        except WebDriverException as e:
            raise RuntimeError(f"Ошибка браузера: {str(e)}")

    @allure.step("Авторизация пользователя {email}")
    def login(self, email: str, password: str) -> None:
        """Выполняет авторизацию пользователя"""
        try:
            self._enter_email(email)
            self._enter_password(password)
            self._click_login_button()
            self._wait_for_authorization_complete()
        except TimeoutException as e:
            allure.attach(str(e), name="auth-error", attachment_type=allure.attachment_type.TEXT)
            raise RuntimeError(f"Таймаут авторизации: {str(e)}")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            raise RuntimeError(f"Ошибка элемента: {str(e)}")

    def _verify_page_loaded(self) -> None:
        """Проверяет загрузку страницы логина"""
        try:
            self._wait_until(
                lambda d: self._page_path in d.current_url,
                message="URL страницы логина не соответствует"
            )
            assert self._is_login_form_present(), "Форма логина не отобразилась"
        except AssertionError as e:
            raise RuntimeError(f"Ошибка загрузки: {str(e)}")

    def _enter_email(self, email: str) -> None:
        """Вводит email в поле ввода"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.EMAIL_INPUT),
                message="Поле email не доступно"
            )
            self._type_text(element, email)
        except TimeoutException as e:
            raise RuntimeError(f"Поле email: {str(e)}")

    def _enter_password(self, password: str) -> None:
        """Вводит пароль в поле ввода"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.PASSWORD_INPUT),
                message="Поле пароля не доступно"
            )
            self._type_text(element, password)
        except TimeoutException as e:
            raise RuntimeError(f"Поле пароля: {str(e)}")

    def _click_login_button(self) -> None:
        """Кликает по кнопке входа"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.LOGIN_BUTTON),
                message="Кнопка входа не доступна"
            )
            self._click(element)
        except TimeoutException as e:
            raise RuntimeError(f"Кнопка входа: {str(e)}")

    def _wait_for_authorization_complete(self) -> None:
        """Ожидает завершения авторизации"""
        expected_url_part = "account"
        try:
            self._wait_until(
                lambda d: expected_url_part in d.current_url.lower(),
                timeout=self._auth_timeout,
                message=f"URL страницы не содержит '{expected_url_part}'. Текущий URL: {self.driver.current_url}"
            )
        except TimeoutException as e:
            raise RuntimeError(f"Таймаут авторизации. Текущий URL: {self.driver.current_url}") from e

    def _is_login_form_present(self) -> bool:
        """Проверяет наличие формы логина"""
        try:
            element = self._wait_until(
                EC.presence_of_element_located(self._locators.LOGIN_FORM),
                timeout=3
            )
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    @allure.step("Переход на страницу восстановления пароля")
    def go_to_password_restore(self) -> None:
        """Переходит на страницу восстановления пароля"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.RESTORE_PASSWORD_LINK),
                message="Ссылка восстановления не доступна"
            )
            self._click(element)
            self._wait_until(lambda d: "forgot-password" in d.current_url)
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка перехода: {str(e)}")

    @allure.step("Переход на страницу регистрации")
    def go_to_register_page(self) -> None:
        """Переходит на страницу регистрации"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.REGISTER_LINK),
                message="Ссылка регистрации не доступна"
            )
            self._click(element)
            self._wait_until(lambda d: "register" in d.current_url)
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка перехода: {str(e)}")

    @allure.step("Переход в конструктор")
    def go_to_constructor(self) -> None:
        """Переходит в конструктор бургеров"""
        try:
            element = self._wait_until(
                EC.element_to_be_clickable(self._locators.CONSTRUCTOR_LINK),
                message="Ссылка конструктора не доступна"
            )
            self._click(element)
            self._wait_until(lambda d: "stellarburgers" in d.current_url)
        except TimeoutException as e:
            raise RuntimeError(f"Ошибка перехода: {str(e)}")