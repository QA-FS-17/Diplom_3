# helpers.py

import requests
from config import API_REGISTER, API_LOGIN, API_USER

def register_user(email: str, password: str, name: str):
    response = requests.post(
        API_REGISTER,
        json={"email": email, "password": password, "name": name}
    )
    return response.json()

def delete_user(email: str, password: str):
    login_response = requests.post(
        API_LOGIN,
        json={"email": email, "password": password}
    )
    token = login_response.json().get("accessToken")
    requests.delete(
        API_USER,
        headers={"Authorization": f"Bearer {token}"}
    )