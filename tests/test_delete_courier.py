import requests
from helpers import BASE_URL, LOGIN_COURIER_ENDPOINT, DELETE_COURIER_ENDPOINT
import allure
from conftest import courier_response


class TestCourierDeletion:


    @allure.title("Успешное удаление курьера")
    @allure.description("Проверка успешного удаления курьера после его создания и входа в систему")
    def test_delete_success(self, courier_response):
        _, courier_data = courier_response
        login_response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login'], "password": courier_data['password']}
        )
        courier_id = login_response.json()['id']
        delete_response = requests.delete(f"{BASE_URL}{DELETE_COURIER_ENDPOINT}{courier_id}")
        assert delete_response.status_code == 200 and delete_response.json() == {"ok": True}


    @allure.title("Удаление курьера без указания ID")
    @allure.description("Проверка обработки ошибки при попытке удаления курьера без указания его ID")
    def test_delete_courier_missing_id(self):
        response = requests.delete(f"{BASE_URL}{DELETE_COURIER_ENDPOINT}")
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для удаления курьера"


    @allure.title("Удаление несуществующего курьера")
    @allure.description("Проверка обработки ошибки при попытке удаления курьера с несуществующим ID")
    def test_delete_courier_nonexistent_id(self):
        nonexistent_courier_id = "99999"  # Убедитесь, что этот ID действительно не существует
        response = requests.delete(f"{BASE_URL}{DELETE_COURIER_ENDPOINT}{nonexistent_courier_id}")
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id нет"


