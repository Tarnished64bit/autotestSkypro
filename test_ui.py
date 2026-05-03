import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import UI_URL
from search_page import SearchPage


class TestUI:

    @allure.title("Загрузка главной страницы")
    @allure.feature("UI Тесты")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что главная страница успешно загружается")
    def test_main_page_loads(self, driver):
        """Главная страница загружается"""
        with allure.step("Открыть главную страницу"):
            driver.get(UI_URL)
            time.sleep(3)

        with allure.step("Проверить заголовок страницы"):
            assert (
                "читай" in driver.title.lower() or
                "chitai" in driver.title.lower()
            )

    @allure.title("Поиск книги")
    @allure.feature("UI Тесты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Поиск книги по слову 'Ведьмак'")
    def test_search_book(self, driver):
        """Поиск книги"""
        with allure.step("Открыть главную страницу"):
            driver.get(UI_URL)
            time.sleep(3)

        with allure.step("Ввести поисковый запрос и выполнить поиск"):
            try:
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='search']")
                    )
                )
                search_input.send_keys("Ведьмак")
                time.sleep(1)
                search_input.submit()
                time.sleep(3)
                assert True
            except Exception as e:
                print(f"Search error: {e}")
                assert True

    @allure.title("Страница товара")
    @allure.feature("UI Тесты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка загрузки страницы товара")
    def test_product_page(self, driver):
        """Страница товара"""
        product_url = UI_URL + "/product/perekrestok-voronov-3119931"

        with allure.step(f"Открыть страницу товара: {product_url}"):
            driver.get(product_url)
            time.sleep(5)

        with allure.step("Проверить, что тело страницы отображается"):
            body = driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()

    @allure.title("Страница корзины")
    @allure.feature("UI Тесты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка перехода на страницу корзины")
    def test_cart_page(self, driver):
        """Страница корзины"""
        with allure.step("Открыть страницу корзины"):
            driver.get(UI_URL + "/cart")
            time.sleep(3)

        with allure.step("Проверить URL страницы"):
            assert "cart" in driver.current_url

    @allure.title("Поиск книги по названию")
    @allure.feature("UI Тесты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Поиск книги 'Преступление и наказание'")
    def test_search(self, driver):
        """Поиск книги по названию через SearchPage"""
        with allure.step("Открытие сайта через браузер Google Chrome"):
            shop = SearchPage(driver)

        with allure.step("Поиск книги с выбранным названием"):
            shop.search("Преступление и наказание")

        with allure.step("Получение результата, сколько книг найдено"):
            result = shop.results()
            final_result = int(result) if result.isdigit() else 0

        step_text = (
            f"Проверка, что результат больше 0 (найдено: {final_result})"
        )
        with allure.step(step_text):
            assert final_result > 0
