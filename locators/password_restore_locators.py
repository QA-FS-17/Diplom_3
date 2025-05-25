# password_restore_locators.py

from selenium.webdriver.common.by import By


class PasswordRestoreLocators:
    RESTORE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and contains(text(), 'Восстановить')]")

    EMAIL_INPUT = (By.CSS_SELECTOR, "input.text.input__textfield.text_type_main-default")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_HIDE_BUTTON = (By.CSS_SELECTOR, "div.input__icon-action svg")
    INPUT_CONTAINER = (By.CSS_SELECTOR, "div.input__container")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
    INPUT_FIELD = (By.CSS_SELECTOR, "div.input")
    INPUT_WRAPPER = (By.CSS_SELECTOR, "div.input")
    TOGGLE_PASSWORD_BTN = (By.XPATH, "//button[contains(@class, 'password-toggle')]")