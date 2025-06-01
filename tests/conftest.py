# conftest.py

import logging
import allure
import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
from config import config
from data import TestUser

logger = logging.getLogger(__name__)

class BrowserNotSupportedError(Exception):
    """Исключение для неподдерживаемых браузеров"""
    pass

class DriverInitError(Exception):
    """Исключение для ошибок инициализации драйвера"""
    pass

@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    """Фикстура для инициализации и завершения работы драйвера"""
    browser = request.param
    driver_instance = None

    try:
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
            })
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-save-password-bubble")
            driver_instance = Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("dom.webnotifications.enabled", False)
            service = FirefoxService(GeckoDriverManager().install())
            driver_instance = webdriver.Firefox(service=service, options=options)

        driver_instance.maximize_window()
        driver_instance.implicitly_wait(10)
        yield driver_instance

    except BrowserNotSupportedError as e:
        pytest.fail(f"Браузер {browser} не поддерживается: {str(e)}")
    except WebDriverException as e:
        allure.attach(str(e), name="WebDriver Error")
        logger.error(f"WebDriver exception: {e}", exc_info=True)
        raise DriverInitError(f"WebDriver error: {str(e)}")
    except Exception as unexpected_error:
        allure.attach(str(unexpected_error), name="Unexpected Error")
        logger.critical(f"Unexpected error: {unexpected_error}", exc_info=True)
        raise

    finally:
        if driver_instance:
            try:
                driver_instance.quit()
            except WebDriverException as quit_error:
                allure.attach(str(quit_error), name="Driver Quit Error")
                logger.error(f"Driver quit error: {quit_error}")
            except Exception as unexpected_quit_error:
                logger.critical(
                    f"Unexpected quit error: {unexpected_quit_error}",
                    exc_info=True
                )

@pytest.fixture
def api_client():
    """Фикстура для HTTP-клиента с обработкой ошибок"""
    session = requests.Session()
    session.headers = {"Content-Type": "application/json"}

    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(api_client):
    """Фикстура для создания тестового пользователя через API"""
    user_data = TestUser().valid_credentials

    try:
        # Регистрация пользователя
        response = api_client.post(
            config.api_register_url,
            json=user_data
        )
        response.raise_for_status()

        yield user_data
    finally:
        # Удаление пользователя
        try:
            login_response = api_client.post(
                config.api_login_url,
                json={"email": user_data["email"], "password": user_data["password"]}
            )
            if login_response.status_code == 200:
                token = login_response.json().get("accessToken")
                api_client.delete(
                    config.api_user_url,
                    headers={"Authorization": f"Bearer {token}"}
                )
        except requests.RequestException as e:
            logger.error(f"Ошибка при удалении тестового пользователя: {e}")

@pytest.fixture
def authenticated_user(driver, test_user):
    """Фикстура для авторизованного пользователя через UI"""
    from pages.login_page import LoginPage

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(test_user["email"], test_user["password"])

    yield {
        "email": test_user["email"],
        "driver": driver
    }

@pytest.fixture
def clean_orders(api_client, authenticated_user):
    """Фикстура для очистки заказов после теста"""
    yield

    try:
        # Получаем токен из кук
        token = api_client.cookies.get("accessToken")
        if token:
            response = api_client.post(
                f"{config.BASE_URL}/api/orders/clear",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200, "Не удалось очистить заказы"
    except requests.RequestException as e:
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