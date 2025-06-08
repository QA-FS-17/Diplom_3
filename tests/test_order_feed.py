# test_order_feed.py

import allure
from config import config
from helpers import is_order_in_list


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Проверка открытия деталей заказа из ленты")
    def test_open_order_details_from_feed(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Добавить ингредиент и оформить заказ"):
            main_page.add_ingredient_to_constructor()
            order_number = main_page.make_order()
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()
            assert order_feed_page.get_current_url() == config.ORDER_FEED_URL

        with allure.step("Открыть детали заказа"):
            order_feed_page.click_first_order()
            assert order_feed_page.is_order_modal_visible()

        with allure.step("Закрыть модальное окно"):
            order_feed_page.close_order_modal()
            assert not order_feed_page.is_order_modal_visible()

    @allure.title("Проверка отображения заказа в истории")
    def test_order_in_history(self, driver, authenticated_user, main_page, profile_page, order_feed_page):
        with allure.step("Добавить ингредиент и оформить заказ"):
            main_page.add_ingredient_to_constructor()
            order_number = main_page.make_order()
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()
            feed_order_numbers = order_feed_page.get_all_order_numbers()

        with allure.step("Проверить наличие заказа в ленте"):
            assert is_order_in_list(feed_order_numbers, order_number)

        with allure.step("Перейти в историю заказов"):
            main_page.go_to_personal_account()
            profile_page.go_to_order_history()
            history_order_numbers = profile_page.get_order_numbers()

        with allure.step("Проверить наличие заказа в истории"):
            assert is_order_in_list(history_order_numbers, order_number)

    @allure.title("Проверка увеличения счетчика 'Выполнено за всё время'")
    def test_total_orders_counter_increase(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Получить начальное значение счетчика"):
            main_page.navigate_to_order_feed()
            initial_total = order_feed_page.get_total_orders_count()

        with allure.step("Создать новый заказ"):
            main_page.navigate_to_constructor()
            main_page.add_ingredient_to_constructor()
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Проверить увеличение счетчика"):
            main_page.navigate_to_order_feed()
            new_total = order_feed_page.get_total_orders_count()
            assert new_total > initial_total

    @allure.title("Проверка увеличения счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter_increase(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Получить начальное значение счетчика"):
            main_page.navigate_to_order_feed()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("Создать новый заказ"):
            main_page.navigate_to_constructor()
            main_page.add_ingredient_to_constructor()
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Проверить увеличение счетчика"):
            main_page.navigate_to_order_feed()
            new_today = order_feed_page.get_today_orders_count()
            assert new_today > initial_today

    @allure.title("Проверка отображения заказа в разделе 'В работе'")
    def test_order_in_progress_section(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Создать новый заказ"):
            main_page.add_ingredient_to_constructor()
            order_number = main_page.make_order()
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()

        with allure.step("Проверить наличие заказа в работе"):
            orders_in_progress = order_feed_page.get_orders_in_progress()
            assert str(order_number) in orders_in_progress