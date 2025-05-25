# profile_page.py

import time
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.profile_page_locators import ProfilePageLocators
from selenium.webdriver.common.by import By
from config import BASE_URL


class ProfilePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.locators = ProfilePageLocators()

    def open(self):
        self.driver.get(f"{BASE_URL}/account/profile")
        return self

    def is_name_input_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.locators.NAME_INPUT),
            "Поле имени не отображается"
        ).is_displayed()

    def wait_for_profile_page(self):
        self.wait.until(
            EC.visibility_of_element_located(ProfilePageLocators.PROFILE_FORM),
            "Форма профиля не загрузилась"
        )

    def is_email_input_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='email']")),
                "Поле email не отобразилось"
            ).is_displayed()
        except TimeoutException:
            try:
                return self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")),
                    "Поле email не отобразилось (альтернативный локатор)"
                ).is_displayed()
            except TimeoutException:
                return False

    def is_active_profile_tab(self) -> bool:
        return self.wait.until(
            EC.presence_of_element_located(self.locators.PROFILE_ACTIVE_TAB),
            "Вкладка профиля не активна"
        ).is_displayed()

    def wait_for_order_history_section(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.locators.ORDER_HISTORY_SECTION),
            "Секция истории заказов не появилась"
        )

    def go_to_order_history(self):
        try:
            self.close_modal_if_present()

            history_link = self.wait.until(
                EC.presence_of_element_located(self.locators.ORDER_HISTORY_LINK)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", history_link)
            self.driver.execute_script("arguments[0].click();", history_link)

            self.wait_for_order_history_section()
        except Exception as e:
            self.driver.save_screenshot("order_history_error.png")
            raise

    def logout(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        logout_btn = self.wait.until(
            lambda d: d.find_element(*self.locators.LOGOUT_BUTTON),
            "Кнопка выхода не найдена после 15 секунд ожидания"
        )

        assert logout_btn.is_displayed(), "Кнопка выхода не отображается"
        logout_btn.click()
        return self

    def wait_for_logout_complete(self):
        self.wait.until(
            EC.url_contains("login"),
            "Не произошел переход на страницу входа после выхода"
        )

    def is_order_history_title_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.locators.ORDER_HISTORY_TITLE),
                "Заголовок истории заказов не отображается"
            ).is_displayed()
        except:
            return False

    def close_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Modal_modal__close_')]"))
            )
            close_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

    def click_logout_button(self):
        logout_button = self.wait.until(
            EC.element_to_be_clickable(self.locators.LOGOUT_BUTTON),
            "Кнопка выхода не найдена или недоступна"
        )
        logout_button.click()
        return self
