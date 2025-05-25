# register_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators
import time


class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "register"

    def open(self):
        self.driver.get(self.base_url + self.url)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(2)

        self.should_be_register_page()

    def should_be_register_page(self):
        print("DEBUG: Проверяем страницу регистрации...")
        print(f"DEBUG: Текущий URL: {self.driver.current_url}")

        assert "register" in self.driver.current_url, \
            f"Неверный URL страницы регистрации. Текущий URL: {self.driver.current_url}"

        self.driver.save_screenshot("register_page_debug.png")
        print("DEBUG: Скриншот страницы сохранен как register_page_debug.png")

        try:
            name_input = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(RegisterPageLocators.NAME_INPUT),
                message="Поле 'Имя' не найдено"
            )
            print(f"DEBUG: Поле Имя найдено: {name_input.get_attribute('outerHTML')}")

            email_input = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(RegisterPageLocators.EMAIL_INPUT),
                message="Поле 'Email' не найдено"
            )
            print(f"DEBUG: Поле Email найдено: {email_input.get_attribute('outerHTML')}")
            assert email_input.get_attribute('type') == 'text', "Поле Email имеет неверный тип"

            password_input = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(RegisterPageLocators.PASSWORD_INPUT),
                message="Поле 'Пароль' не найдено"
            )
            print(f"DEBUG: Поле Пароль найдено: {password_input.get_attribute('outerHTML')}")
            assert password_input.get_attribute('type') == 'password', "Поле Пароль имеет неверный тип"

            register_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(RegisterPageLocators.REGISTER_BUTTON),
                message="Кнопка 'Зарегистрироваться' не найдена или не кликабельна"
            )
            print(f"DEBUG: Кнопка регистрации найдена: {register_button.get_attribute('outerHTML')}")

            login_link = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(RegisterPageLocators.LOGIN_LINK),
                message="Ссылка на страницу входа не найдена"
            )
            print(f"DEBUG: Ссылка на вход найдена: {login_link.get_attribute('href')}")

        except Exception as e:
            print(f"DEBUG: Ошибка при проверке страницы: {str(e)}")
            print(f"DEBUG: HTML страницы (первые 2000 символов):\n{self.driver.page_source[:2000]}")
            raise

    def register(self, name, email, password):
        self.driver.find_element(*RegisterPageLocators.NAME_INPUT).send_keys(name)
        self.driver.find_element(*RegisterPageLocators.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*RegisterPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*RegisterPageLocators.REGISTER_BUTTON).click()

    def should_have_error_message(self, expected_message):
        actual_message = self.driver.find_element(*RegisterPageLocators.ERROR_MESSAGE).text
        assert expected_message in actual_message, \
            f"Ожидалось сообщение '{expected_message}', но получено '{actual_message}'"