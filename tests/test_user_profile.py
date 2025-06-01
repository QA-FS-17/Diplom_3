# test_user_profile.py

import allure
from pages.main_page import MainPage
from pages.profile_page import ProfilePage


@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.story("Переход в личный кабинет")
    def test_go_to_personal_account(self, driver, authenticated_user):
        main_page = MainPage(driver)
        main_page.open()

        main_page.go_to_personal_account()

        assert "account/profile" in driver.current_url, "Не удалось перейти в личный кабинет"

    @allure.story("Переход в историю заказов")
    def test_go_to_order_history(self, driver, authenticated_user):
        profile_page = ProfilePage(driver)
        profile_page.open()

        profile_page.go_to_order_history()

        assert "order-history" in driver.current_url, "Не удалось перейти в историю заказов"

    @allure.story("Выход из аккаунта")
    def test_logout(self, driver, authenticated_user):
        profile_page = ProfilePage(driver)
        profile_page.open()

        profile_page.logout()

        assert "login" in driver.current_url, "Не удалось выйти из аккаунта"