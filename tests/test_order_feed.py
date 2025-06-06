# test_order_feed.py

import allure


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.story("Открытие модального окна с деталями заказа")
    def test_order_details_modal(self, order_feed_page):
        order_feed_page.open()
        order_number = order_feed_page.get_first_order_number()
        order_feed_page.click_order(order_number)
        assert order_feed_page.is_order_modal_visible()

    @allure.story("Отображение заказов пользователя в ленте")
    def test_user_orders_in_feed(self, main_page, order_feed_page, authenticated_user):
        main_page.open()
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()
        order_feed_page.open()
        assert order_number in order_feed_page.get_all_order_numbers()

    @allure.story("Увеличение счетчика 'Выполнено за все время'")
    def test_total_orders_counter(self, main_page, order_feed_page, authenticated_user):
        order_feed_page.open()
        initial_count = order_feed_page.get_total_orders_count()
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()
        order_feed_page.open()
        assert order_feed_page.get_total_orders_count() > initial_count

    @allure.story("Увеличение счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter(self, main_page, order_feed_page, authenticated_user):
        order_feed_page.open()
        initial_count = order_feed_page.get_today_orders_count()
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()
        order_feed_page.open()
        assert order_feed_page.get_today_orders_count() > initial_count

    @allure.story("Отображение заказа в разделе 'В работе'")
    def test_order_in_progress(self, main_page, order_feed_page, authenticated_user):
        main_page.open()
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()
        order_feed_page.open()
        assert order_number in order_feed_page.get_orders_in_progress()