import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from settings import BASE_URL, AUTH_TOKEN


@pytest.fixture
def driver():
    """Фикстура для браузера"""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


class APIClient:
    def __init__(self, token=None):
        self.base_url = BASE_URL
        self.token = token or AUTH_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        if self.token and self.token != "ваш_токен_сюда":
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

    def get(self, endpoint):
        return self.session.get(self.base_url + endpoint)

    def post(self, endpoint, data):
        return self.session.post(self.base_url + endpoint, json=data)

    def put(self, endpoint, data):
        return self.session.put(self.base_url + endpoint, json=data)

    def delete(self, endpoint):
        return self.session.delete(self.base_url + endpoint)
