# conftest.py

import logging
import random
import uuid
import pytest
import requests
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException
from config import config
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    driver = None

    try:
        if browser == "chrome":
            options = uc.ChromeOptions()
            options.add_argument("--disable-popup-blocking")
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "translate": {"enabled": False},
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.geolocation": 2,
            })
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-translate")
            options.add_argument("--disable-save-password-bubble")
            options.add_argument("--disable-single-click-autofill")
            options.add_argument("--disable-features=TranslateUI")

            driver = uc.Chrome(options=options, version_main=None)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("signon.autofillForms", False)
            options.set_preference("browser.translation.detectLanguage", False)
            options.set_preference("intl.accept_languages", "en-US")

            driver = webdriver.Firefox(options=options)

        driver.set_window_position(0, 0)
        driver.maximize_window()
        driver.implicitly_wait(5)
        yield driver

    finally:
        if driver:
            try:
                logger.debug(f"Closing driver, session id: {driver.session_id}")
                driver.quit()
            except WebDriverException as e:
                logger.warning(f"Expected error during driver quit: {str(e)}")
            except OSError as e:
                if "Неверный дескриптор" not in str(e):
                    logger.error(f"OS error during driver quit: {str(e)}")
                    raise


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для HTTP-клиента"""
    session = requests.Session()
    session.headers = {"Content-Type": "application/json"}
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user():
    """Фикстура генерирует тестовые данные пользователя"""
    return {
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "password": f"P@ssw0rd_{uuid.uuid4().hex[:4]}",
        "name": f"User_{uuid.uuid4().hex[:4]}"
    }


@pytest.fixture
def authenticated_user(driver, test_user, api_client):
    """Фикстура авторизованного пользователя с очисткой"""
    # 1. Регистрация через API
    api_client.post(
        config.api_register_url,
        json=test_user,
        timeout=10
    )

    # 2. Авторизация через UI
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(test_user["email"], test_user["password"])

    yield test_user

    # 3. Очистка через API
    try:
        login_response = api_client.post(
            config.api_login_url,
            json={"email": test_user["email"], "password": test_user["password"]},
            timeout=5
        )
        if login_response.status_code == 200:
            api_client.delete(
                config.api_user_url,
                headers={"Authorization": f"Bearer {login_response.json()['accessToken']}"},
                timeout=5
            )
    except requests.exceptions.RequestException as e:
        logger.warning(f"Ошибка при удалении пользователя: {str(e)}")


@pytest.fixture(scope="module")
def registered_user(api_client):
    """Фикстура регистрации пользователя через API (1 раз на файл тестов)"""
    user_data = {
        "email": f"user_{random.randint(1000, 9999)}@test.com",
        "password": "Password123",
        "name": "Test User"
    }

    # Регистрация
    response = api_client.post(
        config.api_register_url,
        json=user_data,
        timeout=5
    )
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя"

    yield user_data

    # Удаление пользователя через API
    try:
        auth_response = api_client.post(
            config.api_login_url,
            json={"email": user_data["email"], "password": user_data["password"]},
            timeout=5
        )
        if auth_response.status_code == 200:
            api_client.delete(
                config.api_user_url,
                headers={"Authorization": f"Bearer {auth_response.json()['accessToken']}"},
                timeout=5
            )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при удалении пользователя: {type(e).__name__}")


@pytest.fixture
def clean_orders(api_client, authenticated_user):
    """Фикстура для очистки заказов после выполнения теста"""
    yield  # Здесь выполняется тест

    try:
        token = api_client.cookies.get("accessToken")
        if token:
            response = api_client.post(
                f"{config.BASE_URL}/api/orders/clear",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200, "Не удалось очистить заказы"
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при очистке заказов: {e}")


# Фикстуры страниц
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
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture
def register_page(driver):
    """Фикстура для страницы регистрации"""
    from pages.register_page import RegisterPage
    return RegisterPage(driver)


@pytest.fixture
def password_restore_page(driver):
    from pages.password_restore_page import PasswordRestorePage
    return PasswordRestorePage(driver)