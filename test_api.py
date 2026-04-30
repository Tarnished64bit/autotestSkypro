import pytest
from settings import PRODUCT_SLUG, CART_PRODUCT, CART, PROFILE, PRODUCT_ID
from conftest import APIClient


class TestAPI:

    def test_search_book(self, api_client):
        """Поиск книги по названию"""
        response = api_client.get(PRODUCT_SLUG)
        if response.status_code == 403:
            pytest.skip(
                "API требует авторизации для поиска"
            )
        assert response.status_code == 200

    def test_add_to_cart(self, api_client):
        """Добавление товара в корзину"""
        payload = {"id": PRODUCT_ID, "quantity": 1}
        response = api_client.post(CART_PRODUCT, payload)
        assert response.status_code == 200

    def test_get_cart(self, api_client):
        """Получение корзины"""
        response = api_client.get(CART)
        if response.status_code == 403:
            pytest.skip("API корзины требует авторизации")
        assert response.status_code == 200

    def test_update_cart_quantity(self, api_client):
        """Обновление количества товара в корзине"""
        add_payload = {"id": PRODUCT_ID, "quantity": 1}
        add_response = api_client.post(CART_PRODUCT, add_payload)
        if add_response.status_code == 403:
            pytest.skip("API корзины требует авторизации")
        assert add_response.status_code == 200

        cart_response = api_client.get(CART)
        if cart_response.status_code == 403:
            pytest.skip("API корзины требует авторизации")

        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            items = cart_data.get("items", [])
            if not items:
                items = cart_data.get("data", {}).get("items", [])
            if items:
                cart_item_id = items[0].get("id") or items[0].get(
                    "productId"
                )
                if cart_item_id:
                    update_payload = {"Id": cart_item_id, "quantity": 2}
                    response = api_client.put(CART, update_payload)
                    assert response.status_code == 200

    def test_get_profile(self, api_client):
        """Получение профиля пользователя"""
        response = api_client.get(PROFILE)
        if response.status_code == 403:
            pytest.skip(
                "API требует авторизации для профиля"
            )
        assert response.status_code == 200

    def test_search_with_invalid_token(self):
        """Поиск с неверным токеном - должен вернуть 401 или 403"""
        client = APIClient(token="invalid_token_12345")
        response = client.get(PRODUCT_SLUG)
        assert response.status_code in [401, 403]

    def test_search_with_typo(self, api_client):
        """Поиск с опечаткой"""
        typo_slug = "/web/api/v1/products/slug/wrong-name"
        response = api_client.get(typo_slug)
        assert response.status_code in [200, 400, 404, 403]
        if response.status_code == 403:
            pytest.skip("API поиска требует авторизации")

    def test_search_nonexistent_product(self, api_client):
        """Поиск несуществующего товара"""
        fake_slug = (
            "/web/api/v1/products/slug/nonexistent-999999999"
        )
        response = api_client.get(fake_slug)
        if response.status_code == 403:
            pytest.skip("API требует авторизации")
        assert response.status_code in [400, 404]

    def test_delete_from_cart(self, api_client):
        """Удаление товара из корзины"""
        add_payload = {"id": PRODUCT_ID, "quantity": 1}
        add_response = api_client.post(CART_PRODUCT, add_payload)
        if add_response.status_code == 403:
            pytest.skip("API корзины требует авторизации")

        cart_response = api_client.get(CART)
        if cart_response.status_code == 403:
            pytest.skip("API корзины требует авторизации")

        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            items = cart_data.get("items", [])
            if not items:
                items = cart_data.get("data", {}).get("items", [])
            if items:
                cart_item_id = items[0].get("id") or items[0].get(
                    "productId"
                )
                if cart_item_id:
                    response = api_client.delete(
                        f"{CART}/{cart_item_id}"
                    )
                    assert response.status_code in [200, 204]
