# register_page_locators.py

from selenium.webdriver.common.by import By

class RegisterPageLocators:
    # Уникальные элементы регистрации
    PAGE_HEADER = (By.XPATH, "//h2[text()='Регистрация']")
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'login')]")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")
    REGISTER_FORM = (By.XPATH, "//form[contains(@class, 'Auth_form')]")