# test_password_restore.py

import allure
from pages.password_restore_page import PasswordRestorePage

@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля со страницы регистрации")
    def test_navigate_to_restore_from_register(self, driver):
        from pages.register_page import RegisterPage
        register_page = RegisterPage(driver).open()
        register_page.go_to_login()
        assert "login" in driver.current_url

    @allure.title("Восстановление пароля")
    def test_password_restoration(self, driver, registered_user):
        PasswordRestorePage(driver).open().restore_password(registered_user.email)
        assert "reset-password" in driver.current_url

    @allure.title("Переключение видимости пароля")
    def test_password_visibility_toggle(self, driver):
        restore_page = PasswordRestorePage(driver).open()

        with allure.step("Проверить активность поля ввода"):
            restore_page.toggle_password_visibility()
            assert restore_page.is_input_active()