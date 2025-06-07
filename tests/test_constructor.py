# test_constructor.py

import allure
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators
from helpers import drag_and_drop


@allure.feature("Основной функционал")
class TestConstructor:
    @allure.title("Переход в конструктор из других разделов")
    def test_navigate_to_constructor(self, register_page, main_page):
        """
        Проверяет переход на главную страницу (конструктор)
        из других разделов приложения
        """
        with allure.step("1. Открыть страницу регистрации"):
            register_page.open()
            assert register_page.is_current_page(), "Не открылась страница регистрации"

        with allure.step("2. Нажать ссылку 'Конструктор' в хедере"):
            register_page.go_to_constructor()

        with allure.step("3. Проверить переход на главную страницу"):
            assert main_page.is_current_page(), "Не произошел переход на главную страницу"
            assert main_page.is_ingredients_section_visible(), "Не отображается секция ингредиентов"

    @allure.title("Переход в ленту заказов из конструктора")
    def test_navigate_to_order_feed(self, driver, main_page, order_feed_page):
        """
        Проверяет переход в раздел "Лента заказов"
        с главной страницы (конструктора)
        """
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Нажать ссылку 'Лента заказов' в хедере"):
            main_page.navigate_to_order_feed()

        with allure.step("Проверить переход в ленту заказов"):
            assert "feed" in driver.current_url
            assert order_feed_page.is_visible(OrderFeedLocators.PAGE_HEADER)

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_open(self, driver, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Кликнуть на первый ингредиент в конструкторе"):
            main_page.click_ingredient()

        with allure.step("Проверить отображение модального окна"):
            assert main_page.is_modal_visible()

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_ingredient_modal_close(self, driver, main_page):
        with allure.step("Открыть и закрыть модальное окно ингредиента"):
            main_page.open()
            main_page.click_ingredient()
            main_page.close_modal()

        with allure.step("Проверить закрытие модального окна"):
            assert not main_page.is_modal_visible()

    @allure.title("Увеличение счетчика при добавлении ингредиента")
    def test_ingredient_counter_increase(self, driver, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        initial_count = main_page.get_ingredient_counter()

        with allure.step("Добавить ингредиент в конструктор"):
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)

        with allure.step("Проверить увеличение счетчика"):
            assert main_page.get_ingredient_counter() == initial_count + 2  # Булки добавляются парами

    @allure.title("Оформление заказа авторизованным пользователем")
    def test_make_order_authenticated(self, driver, authenticated_user, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Добавить ингредиенты в конструктор"):
            ingredient = main_page.find_element(MainPageLocators.INGREDIENT_ITEM)
            constructor_area = main_page.find_element(MainPageLocators.CONSTRUCTOR_AREA)
            drag_and_drop(driver, ingredient, constructor_area)

        with allure.step("Нажать кнопку 'Оформить заказ'"):
            main_page.make_order()

        with allure.step("Проверить отображение номера заказа"):
            assert main_page.is_visible(MainPageLocators.ORDER_NUMBER)