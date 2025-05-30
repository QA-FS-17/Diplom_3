# main_page_locators.py

from selenium.webdriver.common.by import By


class MainPageLocators:
    # Header
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента заказов']/parent::a")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']/parent::a")

    # Ingredients
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/..")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/..")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки']/..")
    INGREDIENT_ITEM = (By.CSS_SELECTOR, "[class^=BurgerIngredient_ingredient]")

    # Constructor
    CONSTRUCTOR_AREA = (By.CSS_SELECTOR, "[class^=BurgerConstructor_basket]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    # Modals
    INGREDIENT_DETAILS_MODAL = (By.CSS_SELECTOR, "[class^=Modal_modal]")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "[class^=Modal_modal] button")
    ORDER_NUMBER = (By.CSS_SELECTOR, "[class^=Modal_orderNumber]")