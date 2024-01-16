import requests
import allure
from data import BASE_URL, LOGIN_COURIER_ENDPOINT, ORDERS_ENDPOINT



class TestGetOrders:


    @allure.title("Получение всех заказов курьера")
    @allure.description("Проверка получения списка всех заказов, назначенных на курьера")
    def test_all_courier_orders(self, courier_response):
        _, courier_data = courier_response
        login_response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login'], "password": courier_data['password']}
        )
        courier_id = login_response.json()['id']
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", params={"courierId": courier_id})
        assert response.status_code == 200 and "orders" in response.json()


    @allure.title("Получение заказов курьера у станций Рокоссовского и Черкизовская")
    @allure.description("Проверка получения списка заказов курьера, находящихся рядом со станциями метро Рокоссовского и Черкизовская")
    def test_get_courier_orders_rokossovskogo_and_cherkizovskaya(sdlf, courier_response):
        _, courier_data = courier_response
        login_response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login'], "password": courier_data['password']}
        )
        assert login_response.status_code == 200, "Ошибка при входе курьера"
        courier_id = login_response.json()['id']
        params = {
            "courierId": courier_id,
            "nearestStation": '["1", "2"]'
        }
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", params=params)
        assert response.status_code == 200 and "orders" in response.json()


    @allure.title("Получение списка из 10 заказов для курьера")
    @allure.description("Проверка получения списка из 10 заказов, доступных для забора курьером")
    def test_get_list_10_orders_to_pick_up_by_courier(self):
        limit = 10
        page = 1
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", params={"limit": limit, "page": page})
        assert response.status_code == 200 and "orders" in response.json()


    @allure.title("Получение 10 заказов для курьера рядом с метро Калужская")
    @allure.description("Проверка получения списка из 10 заказов для курьера, находящихся рядом с метро Калужская")
    def test_get_list_10_orders_to_pick_up_by_courier_near_metro_kaluzhskaya(self):
        limit = 10
        page = 0
        nearest_station = '["110"]'
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}",
                                params={"limit": limit, "page": page, "nearestStation": nearest_station})
        assert response.status_code == 200 and "orders" in response.json()


    @allure.title("Проверка превышения лимита заказов")
    @allure.description("Проверка реакции системы на запрос списка заказов с превышением установленного лимита")
    def test_orders_out_of_limit(self):
        limit = 31
        page = 1
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", params={"limit": limit, "page": page})
        page_info = response.json().get("pageInfo", {})
        assert page_info.get("limit", 0) == 30


    @allure.title("Получение заказов для несуществующего курьера")
    @allure.description("Проверка реакции системы на запрос заказов для курьера с несуществующим идентификатором")
    def test_get_orders_with_nonexistent_courier_id(self):
        nonexistent_courier_id = "99999"
        response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}", params={"courierId": nonexistent_courier_id})
        assert response.status_code == 404 and response.json().get('message') == f"Курьер с идентификатором {nonexistent_courier_id} не найден"







