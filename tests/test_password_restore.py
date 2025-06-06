# test_password_restore.py

import allure
import pytest
import logging

logger = logging.getLogger(__name__)

@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    @allure.story("Переход на страницу восстановления пароля по кнопке 'Восстановить пароль'")
    def test_go_to_password_restore_page(self, login_page):
        login_page.open()
        login_page.go_to_password_restore()
        assert login_page.url_contains("forgot-password")

    @allure.title("Кнопка 'Восстановить' переводит на страницу сброса при вводе email")
    @allure.story("Ввод почты и клик по кнопке 'Восстановить'")
    def test_restore_button_active_with_email(self, login_page, password_restore_page, test_user):
        """
        Проверяет что кнопка 'Восстановить' становится активной
        после ввода валидного email
        """
        with allure.step("1. Открыть страницу восстановления пароля"):
            login_page.open()
            login_page.go_to_password_restore()

        with allure.step("2. Ввести email"):
            password_restore_page.enter_email(test_user["email"])

        with allure.step("3. Проверить активность кнопки"):
            assert password_restore_page.is_restore_button_active(), \
                "Кнопка восстановления должна быть активна после ввода email"

    @allure.title("[BUG] Переход на страницу сброса без ввода email")
    @allure.story("Клик по кнопке 'Восстановить' без ввода почты")
    @pytest.mark.xfail(reason="Известный баг: кнопка активна без email")
    def test_restore_button_active_without_email(self, login_page, password_restore_page):
        """
        Проверяет баг - кнопка 'Восстановить' активна без ввода email
        """
        with allure.step("1. Открыть страницу восстановления пароля"):
            login_page.open()
            login_page.go_to_password_restore()

        with allure.step("2. Проверить активность кнопки без ввода email"):
            assert not password_restore_page.is_restore_button_active(), \
                "Баг: кнопка восстановления активна без ввода email"

    @allure.title("Проверка подсветки поля пароля при взаимодействии")
    @allure.story("Подсветка поля при клике на иконку глаза")
    def test_password_field_becomes_highlighted(self, login_page):
        """
        Проверяет подсветку поля пароля при взаимодействии с иконкой глаза
        """
        # Шаг 1: Открытие страницы
        login_page.open()
        logger.info("Страница открыта.")

        # Шаг 2: Проверка начального состояния
        initial_state = login_page.is_password_field_highlighted()
        logger.info(f"Начальное состояние рамки: {initial_state}")
        assert not initial_state, "Поле пароля должно быть неактивным изначально"

        # Шаг 3: Клик на иконку глаза и проверка изменения состояния
        login_page.click_show_password_button()
        new_state = login_page.is_password_field_highlighted()
        logger.info(f"Состояние рамки после клика: {new_state}")
        assert new_state, "Поле пароля должно стать активным после клика"

        # Дополнительно: проверяем, что тип поля изменился на text (пароль виден)
        attr_type = login_page.get_element_attribute(
            login_page.locators.PASSWORD_INPUT,
            "type"
        )
        logger.info(f"Тип поля после клика: {attr_type}")
        assert attr_type == "text", "Тип поля должен измениться на text"