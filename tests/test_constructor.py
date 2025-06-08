# test_constructor.py

import allure
from pages.main_page import MainPage
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config import config
from helpers import register_new_user, login_user


@allure.feature("Основной функционал")
class TestConstructor:
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_navigate_to_constructor_from_register_page(self, driver):
        register_page = RegisterPage(driver)
        main_page = MainPage(driver)

        with allure.step("1. Открыть страницу регистрации"):
            register_page.open()
            assert register_page.get_current_url() == config.REGISTER_URL

        with allure.step("2. Нажать на ссылку 'Конструктор' в хедере"):
            register_page.click_constructor_link()

        with allure.step("3. Проверить переход на главную страницу"):
            assert main_page.get_current_url() == config.MAIN_PAGE_URL
            assert main_page.is_ingredients_section_visible()

    @allure.title("Переход в ленту заказов по клику на 'Лента заказов'")
    def test_navigate_to_order_feed(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()
            assert main_page.get_current_url() == config.MAIN_PAGE_URL

        with allure.step("2. Нажать на ссылку 'Лента заказов' в хедере"):
            main_page.navigate_to_order_feed()

        with allure.step("3. Проверить переход в раздел ленты заказов"):
            assert main_page.get_current_url() == config.ORDER_FEED_URL

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_open_ingredient_modal(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Кликнуть на первый ингредиент в секции булок"):
            main_page.click_ingredient()

        with allure.step("3. Проверить отображение модального окна"):
            assert main_page.is_modal_visible()

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_close_ingredient_modal(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Открыть модальное окно с ингредиентом"):
            main_page.click_ingredient()
            assert main_page.is_modal_visible()

        with allure.step("3. Закрыть модальное окно"):
            main_page.close_modal()

        with allure.step("4. Проверить что модальное окно закрыто"):
            assert not main_page.is_modal_visible()

    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Получить начальное значение счетчика ингредиента"):
            initial_count = main_page.get_ingredient_counter()

        with allure.step("3. Добавить ингредиент в конструктор"):
            main_page.add_ingredient_to_constructor()

        with allure.step("4. Проверить увеличение счетчика"):
            assert main_page.get_ingredient_counter() > initial_count

    @allure.title("Оформление заказа авторизованным пользователем")
    def test_make_order_by_authenticated_user(self, driver, test_user):
        register_page = RegisterPage(driver)
        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        with allure.step("1. Зарегистрировать нового пользователя"):
            register_new_user(driver, test_user)

        with allure.step("2. Авторизоваться под созданным пользователем"):
            login_user(driver, test_user["email"], test_user["password"])

        with allure.step("3. Добавить ингредиент в конструктор"):
            main_page.add_ingredient_to_constructor()

        with allure.step("4. Нажать кнопку 'Оформить заказ'"):
            order_number = main_page.make_order()

        with allure.step("5. Проверить что появилось окно с номером заказа"):
            assert order_number, "Номер заказа не отображается"