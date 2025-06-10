# test_order_feed.py

import allure


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Открытие деталей заказа из ленты")
    def test_open_order_details_modal(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Подготовка: создать тестовый заказ"):
            main_page.add_ingredient_to_constructor()
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Действие: перейти в ленту заказов и открыть детали"):
            main_page.navigate_to_order_feed()
            order_feed_page.click_first_order()

        with allure.step("Проверка: модальное окно с деталями отображается"):
            assert order_feed_page.is_order_modal_visible()

    @allure.title("Заказ отображается в истории заказов")
    def test_order_appears_in_history(self, authenticated_user, main_page, profile_page):
        with allure.step("1. Подготовка: создать тестовый заказ"):
            main_page.add_ingredient_to_constructor()
            order_number = main_page.make_order()  # Уже содержит ожидание реального номера
            main_page.close_modal()
            assert order_number, "Номер заказа не получен"

        with allure.step("2. Действие: перейти в историю заказов"):
            main_page.go_to_personal_account()
            profile_page.click_order_history_link()
            assert "account/order-history" in profile_page.get_current_url()

        with allure.step("3. Проверка: заказ есть в истории"):
            profile_page.wait_for_order_in_history(order_number)
            assert profile_page.is_order_in_history(order_number), \
                f"Заказ {order_number} не найден в истории"

    @allure.title("Счетчик 'Выполнено за всё время' увеличивается")
    def test_total_orders_counter_increases(self, driver, authenticated_user, main_page, order_feed_page):
        # Подготовка: получить начальное значение
        order_feed_page.open()
        initial_total = order_feed_page.get_total_orders_count()

        # Действие: создать новый заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()
        main_page.close_modal()

        # Проверка: счетчик увеличился
        order_feed_page.open()
        assert order_feed_page.get_total_orders_count() > initial_total

    @allure.title("Счетчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, driver, authenticated_user, main_page, order_feed_page):
        # Подготовка: получить начальное значение
        order_feed_page.open()
        initial_today = order_feed_page.get_today_orders_count()

        # Действие: создать новый заказ
        main_page.open()
        main_page.add_ingredient_to_constructor()
        main_page.make_order()
        main_page.close_modal()

        # Проверка: счетчик увеличился
        order_feed_page.open()
        assert order_feed_page.get_today_orders_count() > initial_today

    @allure.title("Заказ появляется в разделе 'В работе'")
    def test_order_appears_in_progress(self, driver, authenticated_user, main_page, order_feed_page):
        # Подготовка: создать заказ
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()
        main_page.close_modal()

        # Проверка: заказ в разделе "В работе"
        order_feed_page.open()
        assert str(order_number) in order_feed_page.get_orders_in_progress()