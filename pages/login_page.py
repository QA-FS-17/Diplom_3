# login_page.py

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.login_page_locators import LoginPageLocators
from selenium.webdriver.common.by import By


class LoginPage:

    LOGIN_URL = "login"

    def __init__(self, driver):
        self.driver = driver
        self.locators = LoginPageLocators()
        self.wait = WebDriverWait(driver, 15)
        self.base_url = "https://stellarburgers.nomoreparties.site"

    def get_auth_token(self) -> str:
        try:
            return self.driver.execute_script(
                "return localStorage.getItem('accessToken');"
            )
        except Exception as e:
            raise ValueError(f"Не удалось получить токен: {str(e)}")

    def open(self):
        self.driver.get(f"{self.base_url}/{self.LOGIN_URL}")
        self.should_be_login_page()

    def click_restore_password_link(self):
        self.wait.until(
            EC.element_to_be_clickable(self.locators.RESTORE_PASSWORD_LINK)
        ).click()
        self.wait.until(
            EC.url_contains("forgot-password")
        )

    def go_to_login_page(self):
        self.driver.get(f"{self.base_url}/login")
        self.wait.until(
            EC.visibility_of_element_located(self.locators.LOGIN_BUTTON)
        )

    def login(self, email, password):
        try:
            self.close_modal_if_present()

            email_field = self.wait.until(
                EC.visibility_of_element_located(self.locators.EMAIL_INPUT),
                "Поле email не найдено"
            )
            email_field.clear()
            email_field.send_keys(email)

            password_field = self.wait.until(
                EC.visibility_of_element_located(self.locators.PASSWORD_INPUT),
                "Поле пароля не найдено"
            )
            password_field.clear()
            password_field.send_keys(password)

            login_button = self.wait.until(
                EC.presence_of_element_located(self.locators.LOGIN_BUTTON),
                "Кнопка входа не найдена"
            )
            self.driver.execute_script("arguments[0].click();", login_button)

            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/"),
                "Не удалось выполнить авторизацию"
            )

        except Exception as e:
            self.driver.save_screenshot("login_error.png")
            raise

    def click_register_link(self):
        self.wait.until(
            EC.element_to_be_clickable(self.locators.REGISTER_LINK)
        ).click()
        self.wait.until(
            EC.url_contains("register")
        )

    def should_be_login_page(self):
        assert "login" in self.driver.current_url, "Неверный URL страницы логина"
        assert self.is_element_present(self.locators.LOGIN_BUTTON), "Кнопка входа не найдена"
        assert self.is_element_present(self.locators.EMAIL_INPUT), "Поле email не найдено"
        assert self.is_element_present(self.locators.PASSWORD_INPUT), "Поле пароля не найдено"

    def is_login_form_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.locators.LOGIN_FORM),
                "Форма входа не отобразилась"
            ).is_displayed()
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def close_modal_if_present(self):
        try:
            overlay = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr"))
            )
            self.driver.execute_script("arguments[0].remove();", overlay)
        except:
            pass