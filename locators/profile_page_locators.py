# profile_page_locators.py

from selenium.webdriver.common.by import By

class ProfilePageLocators:
    # Уникальные элементы профиля
    PROFILE_FORM = (By.XPATH, "//div[contains(@class, 'Account_account')]")
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Сохранить')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, 'order-history')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    ORDER_HISTORY_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_link')]")
    ORDER_HISTORY_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")