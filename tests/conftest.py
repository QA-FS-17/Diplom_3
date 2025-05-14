# conftest.py

import pytest
import undetected_chromedriver as uc
from selenium import webdriver

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Максимизация окна
    driver.maximize_window()

    yield driver
    driver.quit()