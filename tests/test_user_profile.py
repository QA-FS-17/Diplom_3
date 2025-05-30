# test_user_profile.py

import allure
from pages.main_page import MainPage
from pages.profile_page import ProfilePage

@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.title("Переход в личный кабинет")
    def test_navigate_to_profile(self, authorized_user):
        MainPage(authorized_user).open().go_to_profile()
        assert "account/profile" in authorized_user.current_url

    @allure.title("Просмотр истории заказов")
    def test_order_history(self, authorized_user):
        ProfilePage(authorized_user).open().go_to_order_history()
        assert "order-history" in authorized_user.current_url

    @allure.title("Выход из аккаунта")
    def test_logout(self, authorized_user):
        ProfilePage(authorized_user).open().logout()
        assert "login" in authorized_user.current_url