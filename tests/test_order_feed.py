# test_order_feed.py

import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.story("Открытие модального окна с деталями заказа")
    def test_order_details_modal(self, driver):
        order_feed = OrderFeedPage(driver)
        order_feed.open()

        order_number = order_feed.get_first_order_number()
        order_feed.click_order(order_number)

        assert order_feed.is_order_modal_visible(), "Модальное окно с деталями заказа не открылось"

    @allure.story("Отображение заказов пользователя в ленте")
    def test_user_orders_in_feed(self, driver, authenticated_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)
        profile_page = ProfilePage(driver)

        # Создаем заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()

        # Проверяем в ленте заказов
        order_feed.open()
        order_numbers = order_feed.get_all_order_numbers()

        assert order_number in order_numbers, "Заказ пользователя не отображается в ленте"

    @allure.story("Увеличение счетчика 'Выполнено за все время'")
    def test_total_orders_counter(self, driver, authenticated_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        initial_count = order_feed.get_total_orders_count()

        # Создаем заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()

        # Проверяем счетчик
        order_feed.open()
        new_count = order_feed.get_total_orders_count()

        assert new_count > initial_count, "Счетчик 'Выполнено за все время' не увеличился"

    @allure.story("Увеличение счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter(self, driver, authenticated_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        initial_count = order_feed.get_total_orders_count()

        # Создаем заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()

        # Проверяем счетчик
        order_feed.open()
        new_count = order_feed.get_total_orders_count()

        assert new_count > initial_count, "Счетчик 'Выполнено за сегодня' не увеличился"

    @allure.story("Отображение заказа в разделе 'В работе'")
    def test_order_in_progress(self, driver, authenticated_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        # Создаем заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()

        # Проверяем в разделе "В работе"
        order_feed.open()
        orders_in_progress = order_feed.get_orders_in_progress()

        assert order_number in orders_in_progress, "Заказ не отображается в разделе 'В работе'"