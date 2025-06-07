# test_order_feed.py

import allure
from locators.main_page_locators import MainPageLocators
from helpers import drag_and_drop


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Открытие модального окна с деталями заказа")
    def test_order_details_modal(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Создать тестовый заказ"):
            main_page.open()
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()

        with allure.step("Кликнуть на заказ в ленте"):
            order_feed_page.click_first_order()

        with allure.step("Проверить отображение модального окна"):
            assert order_feed_page.is_order_modal_visible()

    @allure.title("Отображение заказов пользователя в ленте")
    def test_user_orders_in_feed(self, driver, authenticated_user, main_page, order_feed_page, profile_page):
        with allure.step("Создать тестовый заказ"):
            main_page.open()
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)
            main_page.make_order()
            order_number = main_page.get_text(MainPageLocators.ORDER_NUMBER)
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()
            feed_order_numbers = order_feed_page.get_all_order_numbers()

        with allure.step("Проверить наличие заказа в ленте"):
            assert order_number in feed_order_numbers

        with allure.step("Перейти в историю заказов"):
            main_page.go_to_personal_account()
            profile_page.go_to_order_history()
            history_order_numbers = profile_page.get_order_numbers()

        with allure.step("Проверить наличие заказа в истории"):
            assert order_number in history_order_numbers

    @allure.title("Увеличение счетчика 'Выполнено за всё время'")
    def test_total_orders_counter_increase(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Получить начальное значение счетчика"):
            order_feed_page.open()
            initial_total = order_feed_page.get_total_orders_count()

        with allure.step("Создать новый заказ"):
            main_page.navigate_to_constructor()
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Проверить увеличение счетчика"):
            order_feed_page.open()
            new_total = order_feed_page.get_total_orders_count()
            assert new_total == initial_total + 1

    @allure.title("Увеличение счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter_increase(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Получить начальное значение счетчика"):
            order_feed_page.open()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("Создать новый заказ"):
            main_page.navigate_to_constructor()
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Проверить увеличение счетчика"):
            order_feed_page.open()
            new_today = order_feed_page.get_today_orders_count()
            assert new_today == initial_today + 1

    @allure.title("Отображение заказа в разделе 'В работе'")
    def test_order_in_progress_section(self, driver, authenticated_user, main_page, order_feed_page):
        with allure.step("Создать тестовый заказ"):
            main_page.open()
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)
            main_page.make_order()
            order_number = main_page.get_text(MainPageLocators.ORDER_NUMBER)
            main_page.close_modal()

        with allure.step("Перейти в ленту заказов"):
            main_page.navigate_to_order_feed()

        with allure.step("Проверить наличие заказа в разделе 'В работе'"):
            orders_in_progress = order_feed_page.get_orders_in_progress()
            assert order_number in orders_in_progress