# config.py

class Config:
    # Базовые URL
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    # Основные пути
    LOGIN_PATH = "/login"
    REGISTER_PATH = "/register"
    FORGOT_PASSWORD_PATH = "/forgot-password"
    RESET_PASSWORD_PATH = "/reset-password"
    PROFILE_PATH = "/account/profile"
    ORDER_FEED_PATH = "/feed"
    ORDER_HISTORY_PATH = "/account/order-history"

    # API Endpoints
    API_AUTH_REGISTER = "/api/auth/register"
    API_AUTH_LOGIN = "/api/auth/login"
    API_AUTH_USER = "/api/auth/user"
    API_ORDERS = "/api/orders"

    # Время ожидания
    DEFAULT_TIMEOUT = 10  # секунд

    # Тестовые данные
    TEST_EMAIL = "test@example.com"
    TEST_PASSWORD = "Password123"
    TEST_NAME = "Test User"

    @property
    def login_url(self):
        return self.BASE_URL + self.LOGIN_PATH

    @property
    def register_url(self):
        return self.BASE_URL + self.REGISTER_PATH

    @property
    def forgot_password_url(self):
        return self.BASE_URL + self.FORGOT_PASSWORD_PATH

    @property
    def profile_url(self):
        return self.BASE_URL + self.PROFILE_PATH

    @property
    def order_feed_url(self):
        return self.BASE_URL + self.ORDER_FEED_PATH

    @property
    def api_register_url(self):
        return self.BASE_URL + self.API_AUTH_REGISTER

    @property
    def api_login_url(self):
        return self.BASE_URL + self.API_AUTH_LOGIN

    @property
    def api_user_url(self):
        return self.BASE_URL + self.API_AUTH_USER

# Экземпляр конфигурации для использования в проекте
config = Config()