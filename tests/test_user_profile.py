# test_user_profile.py
import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from data import TestUser


@pytest.mark.usefixtures("driver", "test_user")  # Добавили test_user фикстуру
class TestUserProfile:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)
        self.profile_page = ProfilePage(driver)

        # Логиним тестового пользователя
        self.main_page.go_to_login_page()
        self.login_page.login(TestUser.email, TestUser.password)
        self.main_page.wait_for_url_contains("/")

    @allure.title("Проверка перехода в личный кабинет")
    def test_go_to_personal_account(self):
        with allure.step("Клик по кнопке 'Личный кабинет'"):
            self.main_page.go_to_personal_account()
        with allure.step("Проверка URL профиля"):
            assert self.profile_page.is_profile_page()

    @allure.title("Проверка перехода в историю заказов")
    def test_go_to_order_history(self):
        with allure.step("Переход в личный кабинет"):
            self.main_page.go_to_personal_account()
        with allure.step("Переход в историю заказов"):
            self.profile_page.go_to_order_history()
        with allure.step("Проверка URL истории заказов"):
            assert self.profile_page.wait_for_url_contains("/account/order-history")

    @allure.title("Проверка выхода из аккаунта")
    def test_logout(self):
        with allure.step("Переход в личный кабинет"):
            self.main_page.go_to_personal_account()
        with allure.step("Клик по кнопке 'Выход'"):
            self.profile_page.logout()
        with allure.step("Проверка перехода на страницу логина"):
            assert self.login_page.wait_for_url_contains("/login")