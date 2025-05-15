# login_page_locators.py

from selenium.webdriver.common.by import By


class LoginPageLocators:
    # Основные элементы формы входа
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")

    # Ссылки
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]")
    RESTORE_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")

    # Сообщения об ошибках
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")