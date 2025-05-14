# password_restore_locators.py

from selenium.webdriver.common.by import By


class PasswordRestoreLocators:
    # Кнопка перехода на страницу восстановления
    RESTORE_BUTTON = (By.XPATH, '//a[contains(@href, "forgot") and contains(text(), "Восстановить")]')

    # Форма восстановления
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_HIDE_BUTTON = (By.XPATH, "//fieldset[2]//div[contains(@class, 'input__icon')]")