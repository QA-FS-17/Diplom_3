# main_page.py

import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.main_page_locators import MainPageLocators
from config import BASE_URL


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = MainPageLocators()
        self.base_url = BASE_URL
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(BASE_URL)
        self.wait_for_ingredients_loaded()

    def wait_for_ingredients_loaded(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.INGREDIENT_SECTION)
        )

    def is_ingredients_section_visible(self):
        try:
            return self.wait_for_ingredients_loaded(3) is not None
        except TimeoutException:
            return False

    def wait_for_url_contains(self, url_part, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part)
        )

    def _close_modal_if_present(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.locators.MODAL_OVERLAY)
            )
            self.close_modal()
        except TimeoutException:
            pass

    def go_to_constructor(self):
        self._close_modal_if_present()
        self.wait.until(
            EC.element_to_be_clickable(self.locators.CONSTRUCTOR_BUTTON)
        ).click()

    def go_to_order_feed(self):
        self._close_modal_if_present()
        self.wait.until(
            EC.element_to_be_clickable(self.locators.ORDER_FEED_BUTTON)
        ).click()

    def add_bun_to_constructor(self):
        bun = self.wait.until(
            EC.presence_of_element_located(self.locators.BUN_ITEM)
        )
        constructor = self.wait.until(
            EC.presence_of_element_located(self.locators.CONSTRUCTOR_TOP)
        )

        self.driver.execute_script("""
            const dataTransfer = new DataTransfer();
            arguments[0].dispatchEvent(
                new DragEvent('dragstart', { dataTransfer, bubbles: true })
            );
            arguments[1].dispatchEvent(
                new DragEvent('drop', { dataTransfer, bubbles: true })
            );
            arguments[0].dispatchEvent(
                new DragEvent('dragend', { bubbles: true })
            );
        """, bun, constructor)

    def get_bun_counter_value(self):
        try:
            return int(self.wait.until(
                EC.visibility_of_element_located(self.locators.BUN_COUNTER)
            ).text)
        except TimeoutException:
            return 0

    def is_bun_added(self):
        return self.get_bun_counter_value() > 0

    def make_order(self):
        self._close_modal_if_present()
        self.wait.until(
            EC.element_to_be_clickable(self.locators.MAKE_ORDER_BUTTON)
        ).click()

    def get_order_number(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.locators.ORDER_NUMBER)
        ).text

    def close_modal(self):
        self.wait.until(
            EC.element_to_be_clickable(self.locators.MODAL_CLOSE_BUTTON)
        ).click()

    def go_to_personal_account(self):
        try:
            self.close_modal_if_present()

            account_button = self.wait.until(
                EC.presence_of_element_located(self.locators.PERSONAL_ACCOUNT_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", account_button)

            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/account/profile")
            )
        except Exception as e:
            self.driver.save_screenshot("personal_account_error.png")
            raise

    def close_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Modal_modal__close_')]"))
            )
            close_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass