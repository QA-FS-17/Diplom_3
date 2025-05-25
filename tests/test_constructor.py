# test_constructor.py

import pytest
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, LOGIN_URL
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from locators.login_page_locators import LoginPageLocators
from locators.order_feed_locators import OrderFeedLocators


class TestConstructorFromLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.main_page = MainPage(driver)

    @allure.title("Переход в конструктор со страницы логина")
    def test_go_to_constructor_from_login(self, driver):
        with allure.step("Открываем страницу логина"):
            self.driver.get(LOGIN_URL)  # Используем константу
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(LoginPageLocators.LOGIN_BUTTON)
            )
        with allure.step("Кликаем кнопку 'Конструктор'"):
            self.main_page.go_to_constructor()
        with allure.step("Проверяем загрузку конструктора"):
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be(BASE_URL + "/")  # Добавляем слеш для точного сравнения
            )
            assert self.main_page.is_ingredients_section_visible()

    @allure.title("Переход в ленту заказов со страницы логина")
    def test_go_to_order_feed_from_login(self, driver):
        with allure.step("Открываем страницу логина"):
            self.driver.get(f"{BASE_URL}/login")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(LoginPageLocators.LOGIN_BUTTON)
            )
        with allure.step("Кликаем кнопку 'Лента заказов'"):
            self.main_page.go_to_order_feed()
        with allure.step("Проверяем загрузку ленты заказов"):
            assert self.main_page.wait_for_url_contains("/feed"), "Не открылась лента заказов"
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedLocators.ORDER_FEED_SECTION),
                "Заголовок ленты заказов не отобразился"
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OrderFeedLocators.ORDER_LIST),
                "Список заказов не отобразился"
            )

    @allure.title("Проверка открытия модального окна ингредиента")
    def test_modal_open(self, driver):
        self.driver.get(BASE_URL)
        ingredient = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(MainPageLocators.INGREDIENT_BUN)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ingredient)
        modals = self.driver.find_elements(*MainPageLocators.MODAL)
        if modals and modals[0].is_displayed():
            close_button = self.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON)
            self.driver.execute_script("arguments[0].click();", close_button)
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL)
            )
        self.driver.execute_script("arguments[0].click();", ingredient)
        modal = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL),
            "Модальное окно не открылось"
        )
        assert modal.is_displayed(), "Модальное окно должно быть видимым"
        title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_TITLE),
            "Заголовок модального окна не отображается"
        )
        assert title.is_displayed(), "Заголовок должен быть видимым"

    @allure.title("Проверка закрытия модального окна ингредиента")
    def test_modal_close(self, driver):
        self.driver.get(BASE_URL)
        ingredient = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(MainPageLocators.INGREDIENT_BUN)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ingredient)
        self.driver.execute_script("arguments[0].click();", ingredient)
        modal = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL),
            "Модальное окно не открылось"
        )
        close_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON),
            "Кнопка закрытия не найдена"
        )
        self.driver.execute_script("arguments[0].click();", close_button)

        # 7. Проверяем закрытие двумя способами
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located(MainPageLocators.MODAL),
            "Модальное окно не закрылось"
        )
        modal_after_close = self.driver.find_elements(*MainPageLocators.MODAL)
        assert len(modal_after_close) == 0 or not modal_after_close[0].is_displayed(), \
            "Модальное окно должно быть скрыто после закрытия"

    @allure.title("Проверка увеличения счетчика булки при добавлении в конструктор")
    def test_bun_addition(self, driver):
        main_page = MainPage(driver)
        with allure.step("1. Открыть главную страницу"):
            main_page.open()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(main_page.locators.INGREDIENT_SECTION),
                "Секция ингредиентов не загрузилась"
            )
        with allure.step("2. Проверить начальное состояние"):
            initial_counter = main_page.get_bun_counter_value()
            assert initial_counter == 0, f"Начальный счетчик {initial_counter}, ожидалось 0"
            assert not main_page.is_bun_added(), "Булка уже добавлена в конструктор"
        with allure.step("3. Добавить булку в конструктор"):
            main_page.add_bun_to_constructor()
        with allure.step("4. Проверить результат"):
            assert main_page.is_bun_added(), "Булка не была добавлена в конструктор"
            assert main_page.get_bun_counter_value() == 2, "Счетчик булки не увеличился"

    @pytest.mark.usefixtures("ui_auth_user")
    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_authorized_user_can_make_order(self, driver, main_page):
        with allure.step("Проверка авторизации"):
            WebDriverWait(driver, 10).until(
                lambda d: "login" not in d.current_url,
                "Пользователь не авторизован или страница не загрузилась"
            )
        with allure.step("Открываем главную страницу"):
            main_page.open()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.INGREDIENT_SECTION),
                "Секция ингредиентов не загрузилась"
            )
        with allure.step("Добавляем ингредиенты"):
            main_page.add_bun_to_constructor()  # Используем существующий метод
        with allure.step("Оформляем заказ"):
            main_page.make_order()
            order_number = WebDriverWait(driver, 15).until(
                lambda d: main_page.get_order_number(),
                "Не удалось получить номер заказа"
            )
            assert order_number.isdigit(), f"Некорректный номер заказа: {order_number}"