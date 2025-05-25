# main_page_locators.py

from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']/parent::a")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")

    BUN_COUNTER = (By.XPATH, "//*[contains(@class, 'counter_counter__num__3nue1')]")
    BUN_COUNTER_AFTER_DRAG = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6') and contains(., 'Флюоресцентная булка R2-D3')]//p[contains(@class, 'counter_counter__num__3nue1')]")
    INGREDIENT_BUN = (By.XPATH, "//a[.//p[contains(text(), 'булка')]]")
    INGREDIENT_SAUCE = (By.XPATH,
                        "//h2[contains(text(),'Соусы')]/following-sibling::ul//a[contains(@class,'Ingredient_ingredient')]")
    INGREDIENT_MAIN = (By.XPATH,
                       "//h2[contains(text(),'Начинки')]/following-sibling::ul//a[contains(@class,'Ingredient_ingredient')]")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "div[class*='counter_counter__']")

    CONSTRUCTOR_ITEM = (By.CSS_SELECTOR, "div[class*='ConstructorElement_constructor-element']")
    CONSTRUCTOR_TOP = (By.XPATH, "//*[contains(@class, 'constructor-element_pos_top')]")
    CONSTRUCTOR_BOTTOM = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_bun__')][2]")
    CONSTRUCTOR_BUNS = (By.CSS_SELECTOR, "div[class*='BurgerConstructor_bun__']")
    CONSTRUCTOR_MAIN = (By.CSS_SELECTOR, "[class*='BurgerConstructor_main__']")
    CONSTRUCTOR_ITEMS = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_element')]")
    BUN_BY_DRAGGABLE = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6') and contains(., 'Флюоресцентная булка R2-D3')]")

    MODAL = (By.CSS_SELECTOR, "div[class*='Modal_modal__container']")
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title') and contains(text(), 'Детали ингредиента')]")

    INGREDIENT_SECTION = (By.XPATH, "//section[contains(@class, 'BurgerIngredients_ingredients__')]")
    MAIN_SECTION = (By.XPATH, "//h2[contains(text(),'Начинки')]/following-sibling::ul")
    INGREDIENT_NAME = (By.CLASS_NAME, "BurgerIngredient_ingredient__text__yp3dH")

    INGREDIENT_ITEM = (By.CLASS_NAME, "BurgerIngredient_ingredient__1TVf6")
    CONSTRUCTOR_BUN_TOP = (By.XPATH, "//div[contains(@class, 'ConstructorElement_pos_top')]//span[contains(@class, 'constructor-element__text')]")
    CONSTRUCTOR_BUN_BOTTOM = (By.XPATH, "//div[contains(@class, 'ConstructorElement_pos_bottom')]//span[contains(@class, 'constructor-element__text')]")

    LAST_ORDER_NUMBER = (By.CSS_SELECTOR, ".OrderHistory_link__3q9mV:first-child .text_type_digits-default")
    ORDER_FEED_SECTION = (By.CSS_SELECTOR, "section[class*='OrderFeed_orderFeed']")

    FLUORESCENT_BUN = (By.XPATH, "//a[.//p[text()='Флюоресцентная булка R2-D3']]")
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    BUN_INGREDIENT = (By.XPATH, "//div[contains(text(), 'Флюоресцентная булка')]/ancestor::div[contains(@class, 'BurgerIngredient_ingredient')]")
    MAKE_ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button__') and contains(., 'Оформить заказ')]")
    ORDER_NUMBER = (By.XPATH,"//p[contains(@class, 'text_type_digits-large')]")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_overlay')]")

    BUN_ITEM = (By.XPATH, "//a[.//p[text()='Флюоресцентная булка R2-D3']]")
    CONSTRUCTOR_DROP_ZONE = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    MODAL_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")