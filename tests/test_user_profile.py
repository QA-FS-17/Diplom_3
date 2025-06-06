# test_user_profile.py

import allure
from data import TestUser

ERROR_MESSAGE = "Не удалось перейти в личный кабинет"


@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.title("Полный цикл: регистрация -> авторизация -> переход в ЛК")
    def test_register_and_enter_profile(self, register_page, login_page, main_page):
        """Проверка, что после регистрации можно войти в личный кабинет"""
        user_data = TestUser().valid_credentials

        with allure.step("Регистрация нового пользователя"):
            register_page.open()
            register_page.register(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password']
            )

        with allure.step("Авторизация зарегистрированного пользователя"):
            login_page.login(user_data['email'], user_data['password'])
            assert login_page.is_authorized(), "Пользователь не авторизован"

        with allure.step("Проверка перехода в личный кабинет"):
            main_page.go_to_personal_account()
            assert main_page.is_profile_page(), ERROR_MESSAGE

    @allure.title("Переход в историю заказов")
    @allure.story("Профиль пользователя")
    def test_enter_order_history(self, profile_page, authenticated_user):
        """Проверка перехода в историю заказов"""
        with allure.step("Кликнуть на вкладку 'История заказов'"):
            profile_page.go_to_order_history()

        with allure.step("Проверить отображение истории заказов"):
            profile_page.url_should_contain("order-history")
            assert profile_page.is_visible(profile_page.locators.ORDER_LIST), \
                "Список заказов не отображается"

    @allure.title("Выход из аккаунта")
    @allure.story("Авторизация")
    def test_logout(self, profile_page, authenticated_user):
        """Проверка выхода из системы"""
        with allure.step("Кликнуть на кнопку 'Выход'"):
            profile_page.logout()

        with allure.step("Проверить переход на страницу логина"):
            profile_page.url_should_contain("login")
            assert profile_page.is_visible(profile_page.locators.LOGIN_FORM), \
                "Форма входа не отображается после выхода"