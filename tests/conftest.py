# conftest.py

import random
import allure
import pytest
import requests
import undetected_chromedriver as uc
from selenium import webdriver
from config import BASE_URL
from pages.login_page import LoginPage


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
                print(f"Ошибка при закрытии драйвера: {str(e)}")


@pytest.fixture
def api_client():
    """Фикстура для HTTP-клиента"""
    client = requests.Session()
    client.headers = {"Content-Type": "application/json"}
    yield client
    client.close()

@pytest.fixture(scope="function")
def clean_orders(api_client, login):
    """Очистка заказов через API"""
    yield
    try:
        token = api_client.cookies.get("accessToken")
        if token:
            response = api_client.post(
                f"{BASE_URL}/api/orders/clear",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200, "Не удалось очистить заказы"
    except Exception as e:
        allure.attach(str(e), name="Ошибка очистки")

@pytest.fixture
def register_user(api_client):
    """Фикстура для регистрации пользователя через API"""
    user = {
        "email": f"test{random.randint(1000, 9999)}@test.com",
        "password": "Password123",
        "name": "Test User"
    }

    # Регистрация
    response = api_client.post(f"{BASE_URL}/api/auth/register", json=user)
    assert response.status_code == 200

    yield user

    # Удаление
    login_response = api_client.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": user["email"], "password": user["password"]}
    )
    if login_response.status_code == 200:
        token = login_response.json()["accessToken"]
        api_client.delete(
            f"{BASE_URL}/api/auth/user",
            headers={"Authorization": token}
        )


@pytest.fixture
def login(driver, register_user):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(register_user["email"], register_user["password"])

    # Возвращаем токен для использования в API
    yield {
        "token": login_page.get_auth_token(),
        "email": register_user["email"]
    }

    # Очистка
    requests.post(f"{BASE_URL}/api/auth/logout")


# Остальные фикстуры
@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    return MainPage(driver)

@pytest.fixture
def order_feed_page(driver):
    from pages.order_feed_page import OrderFeedPage
    return OrderFeedPage(driver)

@pytest.fixture
def profile_page(driver):
    from pages.profile_page import ProfilePage
    return ProfilePage(driver)


@pytest.fixture
def test_user(api_client):
    """Фикстура для тестового пользователя"""
    user_data = {
        "email": f"test{random.randint(1000, 9999)}@test.com",
        "password": "Password123",
        "name": "Test User"
    }

    # Регистрация
    response = api_client.post(
        f"{BASE_URL}/api/auth/register",
        json=user_data
    )
    assert response.status_code == 200

    yield user_data

    # Удаление
    login_response = api_client.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    if login_response.status_code == 200:
        token = login_response.json().get("accessToken")
        api_client.delete(
            f"{BASE_URL}/api/auth/user",
            headers={"Authorization": f"Bearer {token}"}
        )

@pytest.fixture
def ui_auth_user(driver, register_user):
    """Фикстура для авторизации пользователя через UI"""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(register_user["email"], register_user["password"])
    yield
