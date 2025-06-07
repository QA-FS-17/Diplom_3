# test_password_restore.py

import allure
from locators.password_restore_locators import PasswordRestoreLocators
from data import TestUser


@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_password_restore_page(self, driver, login_page):
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Нажать кнопку 'Восстановить пароль'"):
            login_page.go_to_password_restore()

        with allure.step("Проверить переход на страницу восстановления пароля"):
            assert "forgot-password" in driver.current_url
            assert login_page.is_visible(PasswordRestoreLocators.PAGE_HEADER)

    @allure.title("Ввод почты на странице восстановления пароля")
    def test_enter_email_on_restore_page(self, driver, password_restore_page):
        test_user = TestUser()

        with allure.step("Открыть страницу восстановления пароля"):
            password_restore_page.open()

        with allure.step("Ввести email и нажать кнопку восстановления"):
            password_restore_page.enter_email(test_user.valid_credentials["email"])
            password_restore_page.click_restore_button()

        with allure.step("Проверить переход на страницу сброса пароля"):
            assert "reset-password" in driver.current_url

    @allure.title("Активация поля пароля при нажатии на иконку")
    def test_password_field_activation(self, driver, login_page):
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Проверить начальное состояние поля пароля"):
            assert not login_page.is_password_field_highlighted()

        with allure.step("Нажать на иконку показать/скрыть пароль"):
            login_page.click_show_password_button()

        with allure.step("Проверить подсветку поля пароля"):
            assert login_page.is_password_field_highlighted()