# helpers.py

import uuid
import allure
import requests
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config import API_AUTH_LOGIN, API_AUTH_USER
from selenium.webdriver.remote.webdriver import WebDriver


def create_order_api(token: str) -> int:
    with allure.step("Создание заказа через API"):
        url = "https://stellarburgers.nomoreparties.site/api/orders"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "ingredients": [
                "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка
                "61c0c5a71d1f82001bdaaa72"  # Биокотлета
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["order"]["number"]
        except Exception as e:
            allure.attach(f"Request: {payload}\nResponse: {response.text}",
                          name="API Error")
            raise ValueError(f"Ошибка создания заказа: {str(e)}")

def create_and_login_user(driver, base_url, user_data=None):
    if user_data is None:
        user_data = {
            "name": f"User{uuid.uuid4().hex[:6]}",
            "email": f"test{uuid.uuid4().hex[:8]}@test.com",
            "password": "Pass1234"
        }
    register_page = RegisterPage(driver)
    register_page.base_url = base_url
    with allure.step("UI регистрация"):
        register_page.open()
        register_page.register(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"]
        )
    login_page = LoginPage(driver)
    login_page.base_url = base_url
    with allure.step("UI авторизация"):
        login_page.open()
        login_page.login(
            email=user_data["email"],
            password=user_data["password"]
        )
    def cleanup():
        with allure.step("API очистка"):
            try:
                response = requests.post(
                    API_AUTH_LOGIN,
                    json={
                        "email": user_data["email"],
                        "password": user_data["password"]
                    },
                    timeout=3
                )
                if response.status_code == 200:
                    token = response.json().get("accessToken")
                    requests.delete(
                        API_AUTH_USER,
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=3
                    )
            except Exception as e:
                allure.attach(str(e), name="Ошибка очистки")
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "cleanup": cleanup
    }

def drag_and_drop(driver: WebDriver, source, target) -> None:
    driver.execute_script("""
    function simulateDragDrop(sourceNode, destinationNode) {
        const EVENT_TYPES = {
            DRAG_START: 'dragstart',
            DRAG_OVER: 'dragover',
            DROP: 'drop'
        };
        function createEvent(type) {
            const event = new DragEvent(type, {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            return event;
        }
        sourceNode.dispatchEvent(createEvent(EVENT_TYPES.DRAG_START));
        destinationNode.dispatchEvent(createEvent(EVENT_TYPES.DRAG_OVER));
        destinationNode.dispatchEvent(createEvent(EVENT_TYPES.DROP));
    }
    simulateDragDrop(arguments[0], arguments[1]);
    """, source, target)