from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class SearchPage:
    """Page Object для страницы поиска"""

    def __init__(self, driver):
        """Инициализирует страницу с переданным драйвером"""
        self._driver = driver
        self._driver.get("https://www.chitai-gorod.ru")
        self._driver.maximize_window()
        time.sleep(3)

    @allure.step("Поиск книги по наименованию: {term}")
    def search(self, term):
        """Ввод наименования книги в поле поиска и нажатие кнопки поиска"""
        search_selectors = [
            "input[type='search']",
            "input[name='q']",
            "input.search-input",
            ".search-form__input",
            "#app-search"
        ]

        search_input = None
        for selector in search_selectors:
            try:
                search_input = WebDriverWait(self._driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if search_input:
                    break
            except Exception:
                continue

        if search_input is None:
            search_input = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='search']")
                )
            )

        search_input.clear()
        search_input.send_keys(term)
        time.sleep(1)

        button_selectors = [
            "button[type='submit']",
            "button[aria-label='Поиск']",
            "button.search-form__button-search",
            ".search-button"
        ]

        search_button = None
        for selector in button_selectors:
            try:
                search_button = WebDriverWait(self._driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if search_button:
                    break
            except Exception:
                continue

        if search_button:
            search_button.click()
        else:
            search_input.submit()

        time.sleep(3)

    @allure.step("Получение результата поиска")
    def results(self):
        """Получение количества найденных книг"""
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        count = 0
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-testid='search-result']")
                )
            )
            results = self._driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='search-result']"
            )
            count = len(results)
        except Exception:
            try:
                results = self._driver.find_elements(
                    By.CSS_SELECTOR, ".product-card"
                )
                count = len(results)
            except Exception:
                count = 0

        return str(count)
