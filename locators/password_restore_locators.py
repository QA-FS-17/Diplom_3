# password_restore_locators.py

from selenium.webdriver.common.by import By


class PasswordRestoreLocators:
    # Кнопка перехода на страницу восстановления
    RESTORE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and contains(text(), 'Восстановить')]")

    # Форма восстановления
    EMAIL_INPUT = (By.CSS_SELECTOR, "input.text.input__textfield.text_type_main-default")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_HIDE_BUTTON = (By.CSS_SELECTOR, "div[class*='input__icon'] svg")
    INPUT_CONTAINER = (By.CSS_SELECTOR, ".input")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")