# test_user_profile.py

import allure


@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.title("Переход в личный кабинет")
    def test_go_to_personal_account(self, driver, authenticated_user, main_page):
        with allure.step("Нажать на 'Личный кабинет'"):
            main_page.go_to_personal_account()

        with allure.step("Проверить переход в личный кабинет"):
            assert "account/profile" in driver.current_url

    @allure.title("Переход в историю заказов")
    def test_go_to_order_history(self, driver, authenticated_user, profile_page):
        with allure.step("Открыть страницу профиля"):
            profile_page.open()

        with allure.step("Нажать на 'История заказов'"):
            profile_page.go_to_order_history()

        with allure.step("Проверить переход в историю заказов"):
            assert "order-history" in driver.current_url

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, authenticated_user, profile_page):
        with allure.step("Открыть страницу профиля"):
            profile_page.open()

        with allure.step("Нажать кнопку 'Выход'"):
            profile_page.logout()

        with allure.step("Проверить переход на страницу логина"):
            assert "login" in driver.current_url