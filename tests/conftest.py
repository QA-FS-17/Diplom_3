# conftest.py
import pytest
import requests
from data import TestUser
import undetected_chromedriver as uc
from selenium import webdriver
from config import BASE_URL  # Импортируем BASE_URL из config.py


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.fixture
def api_client():
    client = requests.Session()
    yield client
    client.close()


@pytest.fixture
def test_user(api_client):
    # Регистрация тестового пользователя
    payload = {
        "email": TestUser.email,
        "password": TestUser.password,
        "name": TestUser.name
    }
    response = api_client.post(f"{BASE_URL}/api/auth/register", json=payload)

    # Проверка успешной регистрации
    if response.status_code != 200:
        pytest.fail(f"Failed to register test user: {response.text}")

    yield

    # Удаление тестового пользователя после тестов
    try:
        login_data = {
            "email": TestUser.email,
            "password": TestUser.password
        }
        login_response = api_client.post(f"{BASE_URL}/api/auth/login", json=login_data)

        if login_response.status_code == 200:
            token = login_response.json().get("accessToken")
            if token:
                delete_response = api_client.delete(
                    f"{BASE_URL}/api/auth/user",
                    headers={"Authorization": token}
                )
                if delete_response.status_code != 202:
                    pytest.fail(f"Failed to delete test user: {delete_response.text}")
    except Exception as e:
        pytest.fail(f"Error during test user cleanup: {str(e)}")