# test_order_feed.py

import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage
from data import TestUser
from config import BASE_URL


@pytest.fixture
def clean_test_orders(api_client):
    yield
    # Очистка после всех тестов класса
    login_data = {"email": TestUser.email, "password": TestUser.password}
    response = api_client.post(f"{BASE_URL}/api/auth/login", json=login_data)
    token = response.json()["accessToken"]
    api_client.delete(f"{BASE_URL}/api/orders/all", headers={"Authorization": token})


@pytest.mark.usefixtures("driver", "test_user", "clean_test_orders")
class TestOrderFeed:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)
        self.order_feed_page = OrderFeedPage(driver)
        self.profile_page = ProfilePage(driver)

        # Логин пользователя
        self.main_page.go_to_login_page()
        self.login_page.login(TestUser.email, TestUser.password)
        self.main_page.wait_for_url_contains("/")

    @allure.title("Проверка открытия модального окна деталей заказа")
    @allure.story("Лента заказов")
    def test_open_order_details_modal(self):
        with allure.step("Переход в ленту заказов"):
            self.main_page.go_to_order_feed()

        with allure.step("Открытие деталей заказа"):
            self.order_feed_page.open_order_details()

        with allure.step("Проверка видимости модального окна"):
            assert self.order_feed_page.is_order_modal_visible()

    @allure.title("Проверка закрытия модального окна")
    @allure.story("Лента заказов")
    def test_close_order_details_modal(self):
        self.main_page.go_to_order_feed()
        self.order_feed_page.open_order_details()
        self.order_feed_page.close_order_details()
        assert not self.order_feed_page.is_order_modal_visible()

    @allure.title("Проверка увеличения общего счетчика заказов")
    @allure.story("Счетчики заказов")
    def test_total_orders_counter_increase(self):
        initial_total = self.order_feed_page.get_total_orders_count()
        self.main_page.make_order_successfully()
        assert self.order_feed_page.get_total_orders_count() > initial_total

    @allure.title("Проверка увеличения дневного счетчика заказов")
    @allure.story("Счетчики заказов")
    def test_today_orders_counter_increase(self):
        initial_today = self.order_feed_page.get_today_orders_count()
        self.main_page.make_order_successfully()
        assert self.order_feed_page.get_today_orders_count() > initial_today