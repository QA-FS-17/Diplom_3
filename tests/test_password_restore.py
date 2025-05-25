# test_password_restore.py

import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from locators.login_page_locators import LoginPageLocators
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
            login_page.go_to_login_page()
            login_page.should_be_login_page()
        with allure.step("2. Кликнуть 'Восстановить пароль'"):
            login_page.click_restore_password_link()
        with allure.step("3. Проверить переход на страницу восстановления"):
            assert "forgot-password" in driver.current_url
            assert restore_page.is_element_present(restore_page.locators.EMAIL_INPUT)

    @allure.title("Проверка восстановления пароля")
    @pytest.mark.parametrize("email", ["test@example.com"])
    def test_password_restoration_flow(self, driver, email):
        restore_page = ForgotPasswordPage(driver)
        with allure.step("1. Открыть страницу восстановления"):
            restore_page.go_to_site("forgot-password")
            assert "forgot-password" in driver.current_url
        with allure.step("2. Ввести email и отправить форму"):
            restore_page.enter_email(email)
            restore_page.submit_form()
        with allure.step("3. Проверить переход на страницу сброса"):
            WebDriverWait(driver, 5).until(
                EC.url_contains("reset-password")
            )
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Восстановление пароля']"))
            )

    @allure.title("Подсветка поля пароля")
    def test_password_field_highlighting(self, driver):
        login_page = LoginPage(driver)
        restore_page = ForgotPasswordPage(driver)
        with allure.step("1. Открыть страницу логина"):
            login_page.open()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
            )
        with allure.step("2. Кликнуть на поле пароля"):
            password_field = driver.find_element(*LoginPageLocators.PASSWORD_INPUT)
            password_field.click()
        with allure.step("3. Проверить подсветку поля"):
            # Проверяем родительский элемент поля на наличие класса активности
            parent_div = WebDriverWait(driver, 5).until(
                lambda d: password_field.find_element(By.XPATH, "./..")
            )
            assert "input_status_active" in parent_div.get_attribute("class"), \
                "Поле пароля не подсвечено после клика"