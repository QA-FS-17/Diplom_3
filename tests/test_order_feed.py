# test_order_feed.py

import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from helpers import drag_and_drop
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators
from locators.profile_page_locators import ProfilePageLocators


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("1. Проверка открытия модального окна с деталями заказа")
    def test_order_details_modal(self, driver, login):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        with allure.step("Переходим в ленту заказов"):
            main_page.go_to_order_feed()
            order_feed_page.wait.until(
                EC.presence_of_element_located(OrderFeedLocators.FIRST_ORDER_IN_FEED)
            )
        with allure.step("Кликаем на первый заказ"):
            first_order = order_feed_page.wait.until(
                EC.element_to_be_clickable(OrderFeedLocators.FIRST_ORDER_IN_FEED)
            )
            first_order.click()
        with allure.step("Проверяем что модальное окно открылось"):
            assert order_feed_page.wait.until(
                EC.visibility_of_element_located(OrderFeedLocators.ORDER_MODAL)
            ), "Модальное окно с деталями заказа не открылось"

    @allure.title("2. Проверка отображения заказа в истории заказов")
    def test_order_in_history(self, driver, login, main_page, order_feed_page, profile_page):
        with allure.step("1. Создать и оформить заказ"):
            main_page.open()
            bun = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(MainPageLocators.FLUORESCENT_BUN)
            )
            constructor = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(MainPageLocators.CONSTRUCTOR_AREA)
            )
            driver.execute_script("""
                const dataTransfer = new DataTransfer();
                arguments[0].dispatchEvent(new DragEvent('dragstart', {dataTransfer}));
                arguments[1].dispatchEvent(new DragEvent('drop', {dataTransfer}));
            """, bun, constructor)
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(*MainPageLocators.MAKE_ORDER_BUTTON).is_enabled()
            ).click()
            order_number = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER)
            ).text
            assert order_number, "Не удалось получить номер заказа"
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            ).click()
        with allure.step("2. Проверить заказ в ленте заказов"):
            main_page.go_to_order_feed()
            feed_order = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(OrderFeedLocators.FIRST_ORDER_NUMBER)
            ).text
            assert order_number in feed_order, f"Заказ {order_number} не найден в ленте"
        with allure.step("3. Проверить заказ в истории заказов"):
            main_page.go_to_personal_account()
            profile_page.go_to_order_history()
            history_order = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(ProfilePageLocators.FIRST_ORDER_NUMBER)
            ).text
            assert order_number in history_order, f"Заказ {order_number} не найден в истории"

    @allure.title("3. Проверка увеличения счетчика 'Выполнено за всё время'")
    def test_total_orders_counter(self, driver, login):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        with allure.step("Получить текущее значение счетчика"):
            main_page.go_to_order_feed()
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(OrderFeedLocators.TOTAL_ORDERS_COUNT)
            )
            initial_total = int(driver.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNT).text)
        with allure.step("Создать новый заказ"):
            main_page.open()
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            )
            bun = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.BUN_ITEM)
            )
            constructor = driver.find_element(*MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            drag_and_drop(driver, bun, constructor)
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(*MainPageLocators.MAKE_ORDER_BUTTON).is_enabled()
            )
            main_page.make_order()
            # Ожидаем появление и кликабельность кнопки закрытия
            close_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            )
            # Используем JavaScript для клика, чтобы избежать проблем с перекрытием
            driver.execute_script("arguments[0].click();", close_btn)
            # Ожидаем исчезновение модального окна через ожидание невидимости любого элемента модалки
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        with allure.step("Проверить увеличение счетчика"):
            # Явное ожидание перед переходом
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(*MainPageLocators.CONSTRUCTOR_DROP_ZONE).is_displayed()
            )
            main_page.go_to_order_feed()
            WebDriverWait(driver, 15).until(
                lambda d: int(d.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNT).text) > initial_total,
                message=f"Счетчик не увеличился после создания заказа. Базовое значение: {initial_total}"
            )
            new_total = int(driver.find_element(*OrderFeedLocators.TOTAL_ORDERS_COUNT).text)
            assert new_total > initial_total, \
                f"Ожидалось увеличение счетчика. Начальное значение: {initial_total}, текущее: {new_total}"

    @allure.title("4. Проверка увеличения счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter(self, driver, login):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        with allure.step("Получить текущее значение счетчика"):
            main_page.go_to_order_feed()
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(OrderFeedLocators.TODAY_ORDERS_COUNT)
            )
            initial_today = int(driver.find_element(*OrderFeedLocators.TODAY_ORDERS_COUNT).text)
        with allure.step("Создать новый заказ"):
            main_page.open()
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            )
            bun = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.BUN_ITEM)
            )
            constructor = driver.find_element(*MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            drag_and_drop(driver, bun, constructor)
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(*MainPageLocators.MAKE_ORDER_BUTTON).is_enabled()
            )
            main_page.make_order()
            close_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            )
            driver.execute_script("arguments[0].click();", close_btn)
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        with allure.step("Проверить увеличение счетчика"):
            # Явное ожидание перед переходом
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            )
            main_page.go_to_order_feed()
            WebDriverWait(driver, 15).until(
                lambda d: int(d.find_element(*OrderFeedLocators.TODAY_ORDERS_COUNT).text) > initial_today,
                message=f"Счетчик за сегодня не увеличился. Начальное значение: {initial_today}"
            )
            new_today = int(driver.find_element(*OrderFeedLocators.TODAY_ORDERS_COUNT).text)
            assert new_today > initial_today, \
                f"Ожидалось увеличение счетчика за сегодня. Было: {initial_today}, стало: {new_today}"

    @allure.title("5. Проверка отображения заказа в разделе 'В работе'")
    def test_order_in_progress(self, driver, login):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        with allure.step("1. Создать и оформить заказ"):
            main_page.open()
            bun = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(MainPageLocators.BUN_ITEM)
            )
            constructor = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(MainPageLocators.CONSTRUCTOR_DROP_ZONE)
            )
            drag_and_drop(driver, bun, constructor)
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(MainPageLocators.MAKE_ORDER_BUTTON)
            ).click()
            order_number = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(MainPageLocators.MODAL_ORDER_NUMBER)
            ).text
            assert order_number, "Не удалось получить номер заказа"
            close_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(MainPageLocators.MODAL_CLOSE_BUTTON)
            )
            driver.execute_script("arguments[0].click();", close_btn)
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located(MainPageLocators.MODAL_OVERLAY)
            )
        with allure.step("2. Проверить заказ в разделе 'В работе'"):
            main_page.go_to_order_feed()
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(OrderFeedLocators.IN_PROGRESS_ORDERS)
            )
            in_progress_orders = driver.find_elements(*OrderFeedLocators.IN_PROGRESS_ORDERS)
            order_numbers = [order.text for order in in_progress_orders]
            assert order_number in order_numbers, f"Заказ {order_number} не найден в разделе 'В работе'"