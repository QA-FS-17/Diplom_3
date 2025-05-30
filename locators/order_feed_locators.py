# order_feed_locators.py

from selenium.webdriver.common.by import By

class OrderFeedLocators:
    ORDER_LIST = (By.CSS_SELECTOR, "[class^=OrderFeed_list]")
    ORDER_ITEM = (By.CSS_SELECTOR, "[class^=OrderHistory_link]")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".text_type_digits-default")
    TOTAL_ORDERS = (By.XPATH, "//p[text()='Выполнено за все время']/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[text()='Выполнено за сегодня']/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.CSS_SELECTOR, "[class^=OrderFeed_orderListReady] li")
    ORDER_DETAILS_MODAL = (By.CSS_SELECTOR, "[class^=Modal_modal]")