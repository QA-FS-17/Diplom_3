# password_restore_locators.py

from selenium.webdriver.common.by import By

class PasswordRestoreLocators:
    # Уникальные элементы восстановления пароля
    PAGE_HEADER = (By.XPATH, "//h2[text()='Восстановление пароля']")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    RESTORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon-action')]")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    PASSWORD_INPUT_ACTIVE = (By.XPATH, "//input[@type='text']")
    RESTORE_FORM = (By.XPATH, "//form[contains(@class, 'Auth_form')]")