# order_feed_locators.py

from selenium.webdriver.common.by import By


class OrderFeedLocators:
    ORDER_LIST = (By.XPATH, "//section[contains(@class, 'OrderFeed_orderFeed')]")
    ORDER_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem')][1]")
    ORDER_MODAL = (By.CLASS_NAME, "Modal_modal__")
    ORDER_MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    ORDER_NUMBER_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li[1]")