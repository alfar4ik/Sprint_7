import requests
import pytest
import allure
from data import BASE_URL, ORDERS_ENDPOINT


class TestCreateOrder:
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description("Проверка создания заказа с различными комбинациями цветов и без указания цвета")
    def test_create_order_with_and_without_colors(self, colors):
        order_data = {
            "firstName": "Frank",
            "lastName": "Deltoplan",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 333 11 22",
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "camon play",
            "color": colors
        }
        response = requests.post(
            f"{BASE_URL}{ORDERS_ENDPOINT}",
            json=order_data
        )
        assert response.status_code == 201 and "track" in response.json()
