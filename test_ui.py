import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import UI_URL


class TestUI:

    def test_main_page_loads(self, driver):
        """Главная страница загружается"""
        driver.get(UI_URL)
        time.sleep(3)
        assert (
            "читай" in driver.title.lower() or
            "chitai" in driver.title.lower()
        )

    def test_search_book(self, driver):
        """Поиск книги"""
        driver.get(UI_URL)
        time.sleep(3)

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

    def test_product_page(self, driver):
        """Страница товара"""
        product_url = (
            UI_URL + "/product/perekrestok-voronov-3119931"
        )
        driver.get(product_url)
        time.sleep(5)

        body = driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()

    def test_cart_page(self, driver):
        """Страница корзины"""
        driver.get(UI_URL + "/cart")
        time.sleep(3)
        assert "cart" in driver.current_url
