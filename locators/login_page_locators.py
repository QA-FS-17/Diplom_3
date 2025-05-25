# login_page_locators.py

from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.button_button__33qZ0")

    REGISTER_LINK = (By.XPATH, "//a[contains(@href, 'register')]")
    RESTORE_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, 'forgot-password')]")

    LOGIN_FORM = (By.XPATH, "//form[contains(@class, 'Auth_form__')]")