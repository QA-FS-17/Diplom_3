# test_constructor.py

import allure


@allure.feature("Основной функционал")
class TestMainFunctionality:
    @allure.story("Переход в конструктор")
    def test_go_to_constructor(self, main_page):
        main_page.open()
        main_page.navigate_to_constructor()
        assert main_page.is_current_url_contains("stellarburgers")

    @allure.story("Переход в ленту заказов")
    def test_go_to_order_feed(self, main_page):
        main_page.open()
        main_page.navigate_to_order_feed()
        assert main_page.is_current_url_contains("feed")

    @allure.story("Отображение модального окна с деталями ингредиента")
    def test_ingredient_modal(self, main_page):
        main_page.open()
        main_page.click_ingredient()
        assert main_page.is_modal_visible()

    @allure.story("Закрытие модального окна")
    def test_close_modal(self, main_page):
        main_page.open()
        main_page.click_ingredient()
        main_page.close_modal()
        assert not main_page.is_modal_visible()

    @allure.story("Увеличение счетчика ингредиента")
    def test_ingredient_counter_increase(self, main_page):
        main_page.open()
        initial_count = main_page.get_ingredient_counter()
        main_page.add_ingredient_to_constructor()
        assert main_page.get_ingredient_counter() > initial_count

    @allure.story("Оформление заказа авторизованным пользователем")
    def test_make_order_authenticated(self, main_page, authenticated_user):
        main_page.open()
        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()
        assert order_number.isdigit()