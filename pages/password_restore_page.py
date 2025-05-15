# password_restore_page.py

from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.common.exceptions import NoSuchElementException


class ForgotPasswordPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input.text.input__textfield.text_type_main-default")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_HIDE_BUTTON = (By.CSS_SELECTOR, "div[class*='input__icon'] svg")
    INPUT_CONTAINER = (By.CSS_SELECTOR, ".input")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")

    def go_to_site(self, path=""):
        self.driver.get(f"{self.base_url}{path}")
        self._wait(self.EMAIL_INPUT)

    def enter_email(self, email: str):
        self.fill_field(self.EMAIL_INPUT, email)

    def toggle_password_visibility(self):
        self.click_element(self.SHOW_HIDE_BUTTON)

    def is_password_field_highlighted(self) -> bool:
        # Находим контейнер поля ввода
        input_container = self.driver.find_element(By.CSS_SELECTOR, ".input")

        # Получаем текущий цвет рамки
        current_border = input_container.value_of_css_property("border-color")

        # Сравниваем с цветом подсветки из CSS-переменной
        return current_border == "rgb(76, 76, 255)"  # #4c4cff в RGB

    def submit_form(self):
        self.click_element(self.SUBMIT_BUTTON)

    def is_eye_icon_visible(self):
        return self.driver.find_element(*self.SHOW_HIDE_BUTTON).is_displayed()

    def get_border_color(self):
        return self.driver.find_element(*self.INPUT_CONTAINER).value_of_css_property("border-color")

    def is_password_field_displayed(self) -> bool:
        try:
            return self.driver.find_element(*self.PASSWORD_FIELD).is_displayed()
        except NoSuchElementException:
            return False