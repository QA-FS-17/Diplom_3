# profile_page_locators.py

from selenium.webdriver.common.by import By


class ProfilePageLocators:
    ORDER_HISTORY_LINK = (By.XPATH, "//a[text()='История заказов']")
    FIRST_ORDER_IN_HISTORY = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem')][1]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/account/profile')]")

    ORDER_HISTORY_SECTION = (By.XPATH, "//section[contains(@class, 'order-history')]")
    ORDER_HISTORY_ITEMS = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem__')]")
    ORDER_FEED_SECTION = (By.CSS_SELECTOR, "section[class*='OrderFeed_orderFeed']")

    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PROFILE_ACTIVE_TAB = (By.XPATH, "//a[contains(@class, 'Account_link_active')]")
    ORDER_HISTORY_TITLE = (By.XPATH, "//h2[contains(text(), 'История заказов')]")

    PROFILE_FORM = (By.XPATH, "//div[contains(@class, 'Account_account__')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(text(), 'Выход')]")
    PROFILE_SECTION = (By.XPATH, "//section[contains(@class, 'profile')]")
    ORDER_NUMBERS = (
        By.XPATH,
        "//div[contains(@class, 'OrderHistory_textBox__')]//p[contains(@class, 'text_type_digits-')]"
    )
    FIRST_ORDER_NUMBER = (By.XPATH, "(//p[contains(@class, 'OrderHistory_number__')])[1]")
    ORDER_NUMBER_IN_HISTORY = (By.XPATH, "//p[contains(@class, 'text_type_digits-default')]")