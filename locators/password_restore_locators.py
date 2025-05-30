# password_restore_locators.py

from selenium.webdriver.common.by import By

class PasswordRestoreLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SHOW_HIDE_BUTTON = (By.CSS_SELECTOR, "div.input__icon svg")
    INPUT_ACTIVE = (By.CSS_SELECTOR, "div.input__container.input_status_active")