# main_page_locators.py

from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(text(), 'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(text(), 'Лента Заказов')]")
    INGREDIENT_BUN = (By.XPATH, "//h2[contains(text(), 'Булки')]/following-sibling::div//a[1]")
    INGREDIENT_SAUCE = (By.XPATH, "//h2[contains(text(), 'Соусы')]/following-sibling::div//a[1]")
    INGREDIENT_MAIN = (By.XPATH, "//h2[contains(text(), 'Начинки')]/following-sibling::div//a[1]")
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter_counter__')]")
    MODAL = (By.CLASS_NAME, "Modal_modal__")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close_')]")
    MAKE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_NUMBER = (By.CLASS_NAME, "Modal_modal__title_")