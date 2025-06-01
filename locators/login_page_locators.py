# login_page_locators.py

from selenium.webdriver.common.by import By

class LoginPageLocators:
    # Уникальные элементы страницы логина
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(@href, 'register')]")
    RESTORE_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, 'forgot-password')]")
    LOGIN_FORM = (By.XPATH, "//form[contains(@class, 'Auth_form')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(@href, 'constructor')]")