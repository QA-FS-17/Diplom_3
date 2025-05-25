# order_feed_locators.py

from selenium.webdriver.common.by import By


class OrderFeedLocators:
    ORDER_FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")
    ORDER_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_link')]")
    ORDER_NUMBER = (By.CLASS_NAME, "text_type_digits-default")

    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_overlay__')]")
    MODAL_WINDOW = (By.CSS_SELECTOR, "div[class*='Modal_modal_opened']")
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]")
    MODAL_ORDER_NUMBER = (By.XPATH,
                         "//div[contains(@class, 'Modal_modal__')]//p[contains(@class, 'text_type_digits-')]")
    MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    ORDER_NUMBER_IN_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderNumber')]")

    TOTAL_ORDERS = (By.XPATH,
                   "//p[text()='Выполнено за все время']/following-sibling::p[contains(@class, 'OrderFeed_number')]")
    TODAY_ORDERS = (By.XPATH,
                   "//p[text()='Выполнено за сегодня']/following-sibling::p[contains(@class, 'OrderFeed_number')]")

    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    ORDER_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]//li")

    ORDER_DETAILS_PAGE = (By.XPATH, "//div[contains(@class, 'OrderDetails_page__')]")
    ORDER_NUMBER_ON_PAGE = (By.XPATH, "//p[contains(@class, 'OrderDetails_number__')]")
    ORDER_STATUS = (By.XPATH, "//p[contains(@class, 'OrderDetails_status__')]")
    INGREDIENTS_LIST = (By.XPATH, "//div[contains(@class, 'OrderDetails_ingredients__')]//li")
    BACK_BUTTON = (By.XPATH, "//button[contains(@class, 'OrderDetails_backButton__')]")

    FIRST_ORDER = (By.CSS_SELECTOR, ".OrderHistory_dataBox__1xW9o:first-child")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox__')]")
    ORDER_ITEMS = (By.XPATH, ".//div[contains(@class, 'OrderHistory_link')]")

    ORDER_LIST = (By.XPATH, "//div[contains(@class, 'OrderFeed_list__') or contains(@class, 'OrderFeed_orderList__')]")
    ORDER_FEED_SECTION = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    ORDER_MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(text(),'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p")
    ORDER_NUMBER_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li[1]")

    FIRST_ORDER_IN_FEED = (By.XPATH, "//li[contains(@class, 'OrderHistory_listItem__')][1]")
    MODAL_CLOSE_BUTTON = (
        By.XPATH, "//button[contains(@class, 'Modal_modal__close__')]/*[name()='svg']/..")
    VISIBLE_MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__container__')]//button[contains(@class, 'Modal_modal__close__')]"
    )
    FIRST_ORDER_NUMBER = (By.XPATH, "(//p[contains(@class, 'OrderHistory_number__')])[1]")
    ORDER_NUMBER_IN_LIST = (By.XPATH, "//p[contains(@class, 'OrderHistory_number')]")