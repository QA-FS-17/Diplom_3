# test_password_restore.py

import allure
import pytest
from pages.login_page import LoginPage
from pages.password_recovery_page import ForgotPasswordPage

@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    def test_navigate_to_restore_page(self, driver):
        login_page = LoginPage(driver)
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу логина"):
            login_page.go_to_site()

        with allure.step("2. Кликнуть 'Восстановить пароль'"):
            login_page.click_restore_password_link()

        with allure.step("3. Проверить переход на страницу восстановления"):
            assert "forgot-password" in driver.current_url
            assert restore_page.is_element_present(restore_page.EMAIL_INPUT)

    @allure.title("Восстановление пароля с валидным email")
    @pytest.mark.parametrize("email", ["test@example.com", "user@domain.org"])
    def test_password_restoration_with_valid_email(self, driver, email):
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу восстановления"):
            restore_page.go_to_site("forgot-password")

        with allure.step("2. Ввести email и отправить форму"):
            restore_page.enter_email(email)
            restore_page.submit_form()

        with allure.step("3. Проверить успешную отправку"):
            assert restore_page.is_success_message_displayed()
            assert "reset-password" in driver.current_url

    @allure.title("Подсветка поля пароля")
    def test_password_field_highlighting(self, driver):
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу восстановления"):
            restore_page.go_to_site("forgot-password")

        with allure.step("2. Проверить начальное состояние"):
            assert not restore_page.is_password_field_highlighted()

        with allure.step("3. Кликнуть иконку видимости"):
            restore_page.toggle_password_visibility()

        with allure.step("4. Проверить подсветку"):
            assert restore_page.is_password_field_highlighted()

        with allure.step("5. Проверить снятие подсветки"):
            restore_page.toggle_password_visibility()
            assert not restore_page.is_password_field_highlighted()