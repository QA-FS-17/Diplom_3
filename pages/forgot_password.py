# forgot_password.py

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ForgotPasswordPage(BasePage):
    RESTORE_PASSWORD_BUTTON = (By.XPATH, "//a[text()='Восстановить пароль']")  # Кнопка на странице логина
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")  # Поле ввода email
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Восстановить']")  # Кнопка подтверждения
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")  # Глазик

    def go_to_restore_password_page(self):
        """Переход на страницу восстановления пароля"""
        self.find_element(self.RESTORE_PASSWORD_BUTTON).click()
        assert "forgot-password" in self.driver.current_url, "Не перешли на страницу восстановления пароля!"

    def enter_email_and_submit(self, email):
        """Ввод email и отправка формы"""
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.SUBMIT_BUTTON).click()

    def check_password_visibility_toggle(self):
        """Проверка подсветки поля при клике на 'глазик'"""
        password_input = self.find_element(self.EMAIL_INPUT)
        initial_class = password_input.get_attribute("class")

        self.find_element(self.SHOW_HIDE_PASSWORD_BUTTON).click()
        updated_class = password_input.get_attribute("class")

        assert "input_status_active" in updated_class, "Поле не подсвечивается при активации!"
        assert initial_class != updated_class, "Класс поля не изменился!"