# password_locators.py

from selenium.webdriver.common.by import By


class PasswordRestoreLocators:
    RESTORE_BUTTON = (By.XPATH, "//a[text()='Восстановить пароль']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    SHOW_HIDE_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")