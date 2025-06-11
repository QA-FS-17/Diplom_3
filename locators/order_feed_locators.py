# order_feed_locators.py

from selenium.webdriver.common.by import By

class OrderFeedLocators:
    # Уникальные элементы ленты заказов
    PAGE_HEADER = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText') and contains(text(), 'Лента Заказов')]")
    ORDER_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_link')]")
    ORDER_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
    TOTAL_ORDERS_COUNT = (
        By.XPATH,
        "//div[p[text()='Выполнено за все время:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )

    TODAY_ORDERS_COUNT = (
        By.XPATH,
        "//div[p[text()='Выполнено за сегодня:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )
    ORDERS_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox')]")
    MODAL_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
    FIRST_ORDER_NUMBER = (By.CSS_SELECTOR, "a.OrderHistory_link__1iNby")