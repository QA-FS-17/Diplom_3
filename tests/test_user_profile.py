# test_user_profile.py

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from config import BASE_URL
from locators.profile_page_locators import ProfilePageLocators
from pages.login_page import LoginPage
from pages.main_page import MainPage


@pytest.mark.usefixtures("driver")
class TestUserProfile:
    @pytest.fixture
    def authorized_user(self, driver, test_user):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(test_user["email"], test_user["password"])
        WebDriverWait(driver, 10).until(EC.url_to_be(f"{BASE_URL}/"))
        yield driver
        driver.delete_all_cookies()

    @allure.title("1. Переход в личный кабинет")
    def test_navigate_to_profile(self, authorized_user):
        MainPage(authorized_user).go_to_personal_account()
        current_url = WebDriverWait(authorized_user, 10).until(
            lambda d: d.current_url,
            "Не произошел переход в личный кабинет"
        )
        assert current_url == f"{BASE_URL}/account/profile", \
            f"Ожидался URL {BASE_URL}/account/profile, получен {current_url}"

    @allure.title("2. Переход в историю заказов из ЛК")
    def test_navigate_to_order_history(self, authorized_user):
        MainPage(authorized_user).go_to_personal_account()
        WebDriverWait(authorized_user, 10).until(
            EC.url_to_be(f"{BASE_URL}/account/profile")
        )
        authorized_user.find_element(By.XPATH, "//a[contains(@href, 'order-history')]").click()
        current_url = WebDriverWait(authorized_user, 10).until(
            lambda d: d.current_url,
            "Не произошел переход в историю заказов"
        )
        assert current_url == f"{BASE_URL}/account/order-history", \
            f"Ожидался URL {BASE_URL}/account/order-history, получен {current_url}"

    @allure.title("3. Выход из аккаунта из ЛК")
    def test_user_logout(self, authorized_user, profile_page):
        with allure.step("1. Открыть страницу профиля"):
            profile_page.open()
            WebDriverWait(authorized_user, 10).until(
                EC.visibility_of_element_located(ProfilePageLocators.PROFILE_FORM)
            )
        with allure.step("2. Нажать кнопку выхода"):
            authorized_user.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            logout_btn = WebDriverWait(authorized_user, 15).until(
                EC.element_to_be_clickable(ProfilePageLocators.LOGOUT_BUTTON)
            )
            logout_btn.click()
        with allure.step("3. Проверить переход на страницу входа"):
            WebDriverWait(authorized_user, 10).until(
                EC.url_contains("/login"),
                "Не произошел переход на страницу входа"
            )