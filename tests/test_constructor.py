# test_constructor.py

import allure
from pages.main_page import MainPage


@allure.feature("Основной функционал")
class TestMainFunctionality:
    @allure.story("Переход в конструктор")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.navigate_to_constructor()

        assert "stellarburgers" in driver.current_url, "Не удалось перейти в конструктор"

    @allure.story("Переход в ленту заказов")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.navigate_to_order_feed()

        assert "feed" in driver.current_url, "Не удалось перейти в ленту заказов"

    @allure.story("Отображение модального окна с деталями ингредиента")
    def test_ingredient_modal(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_ingredient()
        is_visible = main_page.is_modal_visible()

        assert is_visible, "Модальное окно с деталями не отображается"

    @allure.story("Закрытие модального окна")
    def test_close_modal(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        main_page.click_ingredient()
        main_page.close_modal()

        assert not main_page.is_modal_visible(), "Модальное окно не закрылось"

    @allure.story("Увеличение счетчика ингредиента")
    def test_ingredient_counter_increase(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        initial_count = main_page.get_ingredient_counter()
        main_page.add_ingredient_to_constructor()
        new_count = main_page.get_ingredient_counter()

        assert new_count > initial_count, "Счетчик ингредиента не увеличился"

    @allure.story("Оформление заказа авторизованным пользователем")
    def test_make_order_authenticated(self, driver, authenticated_user):
        main_page = MainPage(driver)
        main_page.open()

        main_page.add_ingredient_to_constructor()
        order_number = main_page.make_order()

        assert order_number.isdigit(), "Не удалось оформить заказ"