# config.py

class Config:
    """Конфигурация тестового окружения и URL приложения."""

    # Базовые настройки
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    DEFAULT_TIMEOUT = 10  # секунд
    BROWSER_WINDOW_SIZE = "1920x1080"

    # Основные URL страниц
    LOGIN_URL = f"{BASE_URL}/login"
    REGISTER_URL = f"{BASE_URL}/register"
    FORGOT_PASSWORD_URL = f"{BASE_URL}/forgot-password"
    RESET_PASSWORD_URL = f"{BASE_URL}/reset-password"
    PROFILE_URL = f"{BASE_URL}/account/profile"
    ORDER_FEED_URL = f"{BASE_URL}/feed"
    ORDER_HISTORY_URL = f"{BASE_URL}/account/order-history"
    MAIN_PAGE_URL = BASE_URL

    # API Endpoints
    API_BASE = "/api"
    API_AUTH_REGISTER = f"{API_BASE}/auth/register"
    API_AUTH_LOGIN = f"{API_BASE}/auth/login"
    API_AUTH_USER = f"{API_BASE}/auth/user"
    API_AUTH_LOGOUT = f"{API_BASE}/auth/logout"
    API_ORDERS = f"{API_BASE}/orders"
    API_INGREDIENTS = f"{API_BASE}/ingredients"

    # Полные API URL
    @property
    def api_register_url(self):
        return self.BASE_URL + self.API_AUTH_REGISTER

    @property
    def api_login_url(self):
        return self.BASE_URL + self.API_AUTH_LOGIN

    @property
    def api_user_url(self):
        return self.BASE_URL + self.API_AUTH_USER

    @property
    def api_orders_url(self):
        return self.BASE_URL + self.API_ORDERS

    # Тестовые данные пользователя
    class TestData:
        DEFAULT_PASSWORD = "Password123"
        DEFAULT_NAME = "Test User"

        @staticmethod
        def generate_email():
            import uuid
            return f"user_{uuid.uuid4().hex[:8]}@example.com"

    # Настройки отчетов
    ALLURE_RESULTS_DIR = "allure-results"
    SCREENSHOTS_DIR = "screenshots"


# Экземпляр конфигурации для использования в проекте
config = Config()