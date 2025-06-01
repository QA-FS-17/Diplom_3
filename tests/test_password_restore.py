# test_password_restore.py

import allure
from pages.login_page import LoginPage
from pages.password_restore_page import PasswordRestorePage


@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.story("Переход на страницу восстановления пароля")
    def test_go_to_password_restore_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.go_to_password_restore()

        assert "forgot-password" in driver.current_url, "Не удалось перейти на страницу восстановления пароля"

    @allure.story("Восстановление пароля с валидным email")
    def test_restore_password_with_valid_email(self, driver, test_user):
        login_page = LoginPage(driver)
        restore_page = PasswordRestorePage(driver)

        login_page.open()
        login_page.go_to_password_restore()
        restore_page.restore_password(test_user["email"])

        assert "reset-password" in driver.current_url, "Не удалось отправить форму восстановления"

    @allure.story("Подсветка поля пароля при клике на иконку")
    def test_password_field_highlight(self, driver):
        restore_page = PasswordRestorePage(driver)
        restore_page.open()

        restore_page.toggle_password_visibility()
        is_highlighted = restore_page.is_password_field_highlighted()

        assert is_highlighted, "Поле пароля не подсвечивается при активации"