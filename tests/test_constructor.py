# test_constructor.py
import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from data import TestUser


@pytest.mark.usefixtures("driver", "test_user")
class TestConstructor:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)

        # Логиним пользователя перед тестами
        self.main_page.go_to_login_page()
        self.login_page.login(TestUser.email, TestUser.password)
        self.main_page.wait_for_url_contains("/")

    @allure.title("Проверка перехода в конструктор")
    @allure.story("Основной функционал")
    def test_go_to_constructor(self):
        with allure.step("Кликнуть на кнопку 'Конструктор'"):
            self.main_page.go_to_constructor()
        with allure.step("Проверить URL страницы"):
            assert self.main_page.wait_for_url_contains("/")

    @allure.title("Проверка перехода в ленту заказов")
    @allure.story("Основной функционал")
    def test_go_to_order_feed(self):
        with allure.step("Кликнуть на кнопку 'Лента заказов'"):
            self.main_page.go_to_order_feed()
        with allure.step("Проверить URL страницы"):
            assert self.main_page.wait_for_url_contains("/feed")

    @allure.title("Проверка модального окна ингредиента")
    @allure.story("Работа с ингредиентами")
    def test_ingredient_modal(self):
        with allure.step("Выбрать ингредиент 'Булки'"):
            self.main_page.select_ingredient("bun")
        with allure.step("Проверить отображение модального окна"):
            assert self.main_page.is_modal_visible()
        with allure.step("Закрыть модальное окно"):
            self.main_page.close_modal()
        with allure.step("Проверить закрытие модального окна"):
            assert not self.main_page.is_modal_visible()

    @allure.title("Проверка счетчика ингредиентов")
    @allure.story("Работа с ингредиентами")
    def test_ingredient_counter(self):
        with allure.step("Получить начальное значение счетчика"):
            initial_count = self.main_page.get_ingredient_counter("bun")
        with allure.step("Добавить ингредиент 'Булки'"):
            self.main_page.select_ingredient("bun")
        with allure.step("Проверить увеличение счетчика"):
            assert self.main_page.get_ingredient_counter("bun") == initial_count + 1
        with allure.step("Закрыть модальное окно"):
            self.main_page.close_modal()

    @allure.title("Проверка оформления заказа")
    @allure.story("Оформление заказов")
    def test_make_order(self):
        with allure.step("Добавить ингредиенты в заказ"):
            self.main_page.select_ingredient("bun")
            self.main_page.select_ingredient("sauce")
        with allure.step("Оформить заказ"):
            self.main_page.make_order()
        with allure.step("Проверить отображение модального окна с номером"):
            assert self.main_page.is_modal_visible()
            order_number = self.main_page.get_order_number()
            assert order_number.isdigit()
        with allure.step("Закрыть модальное окно"):
            self.main_page.close_modal()