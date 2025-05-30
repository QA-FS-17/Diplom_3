# profile_page_locators.py

from selenium.webdriver.common.by import By

class ProfilePageLocators:
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, 'profile')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, 'order-history')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    ORDER_HISTORY_ITEM = (By.CSS_SELECTOR, "[class^=OrderHistory_listItem]")
    PROFILE_FORM = (By.CSS_SELECTOR, "[class^=Profile_profile]")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-number")