# test_order_feed.py

import allure

from locators.order_feed_locators import OrderFeedLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Просмотр деталей заказа")
    def test_view_order_details(self, driver):
        order_feed = OrderFeedPage(driver).open()

        with allure.step("Открыть детали заказа"):
            order_number = order_feed.get_order_number()
            order_feed.open_order_details()
            assert order_feed.is_visible(OrderFeedLocators.ORDER_DETAILS_MODAL)

        with allure.step("Проверить номер заказа"):
            assert order_number in driver.page_source

    @allure.title("Проверка счетчиков заказов")
    def test_orders_counters(self, authorized_user):
        main_page = MainPage(authorized_user).open()
        order_feed = OrderFeedPage(authorized_user)

        with allure.step("Получить начальные значения счетчиков"):
            initial_total = order_feed.open().get_total_orders_count()
            initial_today = order_feed.get_today_orders_count()

        with allure.step("Создать новый заказ"):
            main_page.open().add_ingredient("bun").make_order()
            main_page.close_modal()

        with allure.step("Проверить увеличение счетчиков"):
            order_feed.open()
            assert order_feed.get_total_orders_count() > initial_total
            assert order_feed.get_today_orders_count() > initial_today