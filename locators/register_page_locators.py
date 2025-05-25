# register_page_locators.py

from selenium.webdriver.common.by import By


class RegisterPageLocators:
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//label[contains(text(),'Email')]/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and @name='Пароль']")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(),'Зарегистрироваться')]")

    LOGIN_LINK = (By.XPATH, "//a[contains(@href,'login')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class,'input__error')]")