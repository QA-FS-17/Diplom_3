# data.py

import uuid
from typing import Dict, Literal

# Константы для идентификаторов ингредиентов
INGREDIENT_IDS = {
    "bun": {
        "fluorescent": "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка
        "crust": "61c0c5a71d1f82001bdaaa6f"  # Космическая краторная булка
    },
    "sauce": {
        "spicy": "61c0c5a71d1f82001bdaaa72",  # Соус Spicy-X
        "sour_cream": "61c0c5a71d1f82001bdaaa71"  # Соус традиционный галактический
    },
    "main": {
        "biocutlet": "61c0c5a71d1f82001bdaaa73",  # Биокотлета из марсианской Магнолии
        "beef": "61c0c5a71d1f82001bdaaa74"  # Говяжий метеорит
    }
}

# Типы для аннотаций
IngredientType = Literal["bun", "sauce", "main"]
IngredientName = Literal["fluorescent", "crust", "spicy", "sour_cream", "biocutlet", "beef"]


class TestUser:
    """Класс для генерации тестовых данных пользователя."""

    DEFAULT_PASSWORD = "SecurePassword123!"
    DEFAULT_NAME = "Test User"

    def __init__(self):
        self._credentials = None

    @staticmethod
    def generate_test_email(prefix: str = "test") -> str:
        """Генерирует уникальный тестовый email.

        Args:
            prefix: Префикс для email (по умолчанию "test")

        Returns:
            Строка с email в формате prefix_uuid@example.com
        """
        return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

    @property
    def valid_credentials(self) -> Dict[str, str]:
        """Возвращает валидные учетные данные для регистрации/авторизации.

        Returns:
            Словарь с email, password и name
        """
        if not self._credentials:
            self._credentials = {
                "email": self.generate_test_email(),
                "password": self.DEFAULT_PASSWORD,
                "name": self.DEFAULT_NAME
            }
        return self._credentials

    @property
    def invalid_passwords(self) -> Dict[str, str]:
        """Возвращает набор невалидных паролей с описанием ошибок.

        Returns:
            Словарь {описание_ошибки: пароль}
        """
        return {
            "too_short": "Short1",
            "no_digits": "NoDigits!",
            "no_uppercase": "lowercase123",
            "no_special_chars": "MissingSpecial1"
        }


def get_ingredient_id(ingredient_type: IngredientType, name: IngredientName) -> str:
    """Возвращает идентификатор ингредиента по типу и названию.

    Args:
        ingredient_type: Тип ингредиента ('bun', 'sauce', 'main')
        name: Название конкретного ингредиента

    Returns:
        Строка с идентификатором ингредиента

    Raises:
        KeyError: Если ингредиент не найден
    """
    try:
        return INGREDIENT_IDS[ingredient_type][name]
    except KeyError as e:
        raise KeyError(f"Ingredient {name} of type {ingredient_type} not found") from e