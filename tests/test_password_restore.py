# test_password_restore.py

import allure
import pytest
from pages.forgot_password import ForgotPasswordPage
from pages.login_page import LoginPage


@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_restore_page(self, driver):
        login_page = LoginPage(driver)
        login_page.go_to_site()
        login_page.click_restore_password_link()

        restore_page = ForgotPasswordPage(driver)
        assert "forgot-password" in driver.current_url, "Не открылась страница восстановления!"

    @allure.title("Восстановление пароля с валидным email")
    def test_restore_password_with_valid_email(self, driver):
        restore_page = ForgotPasswordPage(driver)
        restore_page.go_to_site("forgot-password")  # Предполагаем метод для прямого перехода
        restore_page.enter_email_and_submit("valid_email@example.com")
        assert "reset-password" in driver.current_url, "Не появился экран подтверждения!"

    @allure.title("Проверка подсветки поля пароля")
    def test_password_field_highlight(self, driver):
        restore_page = ForgotPasswordPage(driver)
        restore_page.go_to_site("forgot-password")
        restore_page.check_password_visibility_toggle()