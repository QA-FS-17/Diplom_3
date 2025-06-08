# test_user_profile.py

import allure
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from config import config
from helpers import login_user


@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.title("Переход в личный кабинет")
    def test_navigate_to_personal_account(self, driver, test_user):
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        with allure.step("Авторизация пользователя"):
            login_user(driver, test_user["email"], test_user["password"])

        with allure.step("Переход в личный кабинет"):
            login_page.go_to_personal_account()

        with allure.step("Проверка загрузки страницы профиля"):
            assert profile_page.is_profile_form_visible(), "Форма профиля не отображается"
            assert profile_page.get_current_url() == config.PROFILE_URL, "URL не соответствует странице профиля"

    @allure.title("Переход в историю заказов")
    def test_navigate_to_order_history(self, driver, test_user):
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        with allure.step("Авторизация пользователя"):
            login_user(driver, test_user["email"], test_user["password"])

        with allure.step("Переход в личный кабинет"):
            login_page.go_to_personal_account()

        with allure.step("Переход в историю заказов"):
            profile_page.go_to_order_history()

        with allure.step("Проверка перехода на страницу истории"):
            assert "account/order-history" in profile_page.get_current_url(), "URL не соответствует странице истории заказов"

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, test_user):
        login_page = LoginPage(driver)
        profile_page = ProfilePage(driver)

        with allure.step("Авторизация пользователя"):
            login_user(driver, test_user["email"], test_user["password"])

        with allure.step("Переход в личный кабинет"):
            login_page.go_to_personal_account()

        with allure.step("Выход из аккаунта"):
            profile_page.logout()

        with allure.step("Проверка перехода на страницу входа"):
            assert login_page.get_current_url() == config.LOGIN_URL, "URL не соответствует странице входа"
            assert login_page.is_login_form_visible(), "Форма входа не отображается"