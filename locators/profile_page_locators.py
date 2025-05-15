# profile_page_locators.py

from selenium.webdriver.common.by import By


class ProfilePageLocators:
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, '/account/order-history')]")
    FIRST_ORDER_IN_HISTORY = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem')][1]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/account/profile')]")