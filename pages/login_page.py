# login_page.py

import allure
import logging
from .base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url_suffix="login")
        self.locators = LoginPageLocators()
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Проверка загрузки страницы входа")
    def _verify_page_loaded(self) -> None:
        """Проверка загрузки страницы входа"""
        elements_to_check = [
            self.locators.LOGIN_FORM,
            self.locators.EMAIL_INPUT,
            self.locators.PASSWORD_INPUT
        ]

        for locator in elements_to_check:
            self.wait_until_visible(locator)

    @allure.step("Открыть страницу логина")
    def open(self) -> None:
        """Открывает страницу логина"""
        super().open()
        self._verify_page_loaded()

    @allure.step("Проверить видимость формы логина")
    def is_login_form_visible(self) -> bool:
        """Проверяет видимость формы логина"""
        return self.is_visible(self.locators.LOGIN_FORM)

    @allure.step("Проверить наличие поля пароля")
    def is_password_field_present(self) -> bool:
        """Проверяет наличие поля пароля"""
        return self.is_present(self.locators.PASSWORD_INPUT)

    @allure.step("Перейти на страницу восстановления пароля")
    def go_to_password_restore(self) -> None:
        """Переходит на страницу восстановления пароля"""
        self.click(self.locators.RESTORE_PASSWORD_LINK)
        self.wait_until_url_contains("forgot-password")

    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self) -> None:
        """Переходит в личный кабинет"""
        self.logger.info("Переход в личный кабинет")
        self.click(self.locators.PERSONAL_ACCOUNT_BUTTON)
        self.wait_until_url_contains("account/profile")

    @allure.step("Авторизоваться как {email}")
    def login(self, email: str, password: str) -> None:
        """Выполняет авторизацию пользователя"""
        self.logger.info(f"Авторизация пользователя {email}")
        self.type_text(self.locators.EMAIL_INPUT, email)
        self.type_text(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        self.wait_until_url_contains("/")

    @allure.step("Проверить подсветку поля пароля")
    def is_password_field_highlighted(self) -> bool:
        """Проверяет подсветку поля пароля"""
        try:
            self.wait_until_visible(self.locators.ACTIVE_FIELD, timeout=3)
            return True
        except TimeoutException:
            return False

    @allure.step("Нажать кнопку показать пароль")
    def click_show_password_button(self) -> None:
        """Нажимает кнопку показать пароль"""
        initial_state = self.is_password_field_highlighted()
        self.click(self.locators.SHOW_PASSWORD_BUTTON)

        def state_changed():
            return self.is_password_field_highlighted() != initial_state

        self.wait_for_condition(
            state_changed,
            timeout=5,
            message="Состояние подсветки не изменилось"
        )