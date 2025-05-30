# conftest.py

import allure
import pytest
import requests
import uc
from selenium import webdriver
from config import BASE_URL, API_REGISTER, API_LOGIN, API_USER
from data import TestUser


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    driver = None
    try:
        if browser == "chrome":
            options = uc.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
            })
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-save-password-bubble")
            driver = uc.Chrome(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            driver = webdriver.Firefox(options=options)

        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver

    except Exception as e:
        pytest.fail(f"Ошибка инициализации драйвера: {str(e)}")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                allure.attach(str(e), name="Ошибка закрытия драйвера")


@pytest.fixture
def test_user():
    return TestUser()


@pytest.fixture
def registered_user(driver, test_user):
    from pages.register_page import RegisterPage
    register_page = RegisterPage(driver)
    register_page.open().register(
        name=test_user.name,
        email=test_user.email,
        password=test_user.password
    )
    yield test_user

    # Удаление через API
    login_response = requests.post(
        API_LOGIN,
        json={"email": test_user.email, "password": test_user.password}
    )
    token = login_response.json()["accessToken"]
    requests.delete(
        API_USER,
        headers={"Authorization": f"Bearer {token}"}
    )


@pytest.fixture
def authorized_user(driver, registered_user):
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.open().login(registered_user.email, registered_user.password)
    yield driver
    requests.post(f"{BASE_URL}/api/auth/logout")