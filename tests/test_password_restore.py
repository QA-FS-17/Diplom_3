# test_password_restore.py

import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from pages.login_page import LoginPage
from pages.password_restore_page import ForgotPasswordPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    def test_navigate_to_restore_page(self, driver):
        login_page = LoginPage(driver)
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу логина"):
            login_page.go_to_login_page()  # Используем метод для перехода на страницу логина

        with allure.step("2. Кликнуть 'Восстановить пароль'"):
            login_page.click_restore_password_link()

        with allure.step("3. Проверить переход на страницу восстановления"):
            assert "forgot-password" in driver.current_url, (
                f"Ожидался URL с 'forgot-password', получен: {driver.current_url}"
            )
            assert restore_page.is_element_present(restore_page.EMAIL_INPUT), (
                "Поле ввода email не найдено"
            )

    @allure.title("Проверка восстановления пароля: ввод email и клик по кнопке 'Восстановить'")
    @pytest.mark.parametrize("email", ["test@example.com"])
    def test_password_restoration_flow(self, driver, email):
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу восстановления пароля"):
            restore_page.go_to_site("forgot-password")
            assert "forgot-password" in driver.current_url

        with allure.step("2. Ввести email и нажать кнопку 'Восстановить'"):
            restore_page.enter_email(email)
            restore_page.submit_form()

        with allure.step("3. Проверить переход на страницу сброса пароля и дождаться загрузки страницы"):
            # Ждем перехода по URL
            WebDriverWait(driver, 5).until(
                EC.url_contains("reset-password"),
                message="Не произошел переход на страницу reset-password"
            )
            # Ждем появления заголовка "Восстановление пароля"
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Восстановление пароля']")),
                message="Страница сброса пароля не загрузилась"
            )

    @allure.title("Подсветка поля пароля при взаимодействии с иконкой видимости")
    def test_password_field_highlighting(self, driver):
        restore_page = ForgotPasswordPage(driver)

        with allure.step("1. Открыть страницу восстановления пароля"):
            restore_page.go_to_site("login")
            assert restore_page.is_password_field_displayed(), "Поле пароля не отображается"

        with allure.step("2. Проверить исходное состояние (без подсветки)"):
            assert not restore_page.is_password_field_highlighted(), (
                "Поле уже подсвечено в начальном состоянии"
            )

        with allure.step("3. Кликнуть иконку видимости пароля"):
            assert restore_page.is_eye_icon_visible(), "Иконка видимости не найдена"
            restore_page.toggle_password_visibility()

        with allure.step("4. Проверить появление подсветки"):
            WebDriverWait(driver, 3).until(
                lambda _: restore_page.is_password_field_highlighted(),
                "Подсветка не появилась после клика"
            )

        with allure.step("5. Проверить снятие подсветки при повторном клике"):
            restore_page.toggle_password_visibility()
            WebDriverWait(driver, 3).until_not(
                lambda _: restore_page.is_password_field_highlighted(),
                "Подсветка не исчезла после второго клика"
            )