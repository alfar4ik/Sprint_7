import requests
import allure
from data import BASE_URL, CREATE_COURIER_ENDPOINT



class TestCourierCreation:


    @allure.title("Создание курьера успешно")
    @allure.description("Проверка успешного создания курьера с корректными данными")
    def test_create_courier_success(self, courier_response):
        response, _ = courier_response
        assert response.status_code == 201 and response.json() == {"ok": True}


    @allure.title("Создание курьера без логина")
    @allure.description("Проверка невозможности создания курьера без указания логина")
    def test_create_courier_no_login(self, courier_response):
        _, courier_data = courier_response
        modified_data = courier_data.copy()
        modified_data.pop('login', None)
        response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=modified_data)
        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для создания учетной записи"


    @allure.title("Создание курьера с дублирующимся логином")
    @allure.description("Проверка ошибки при попытке создать курьера с уже существующим логином")
    def test_create_courier_duplicate_login(self, courier_response):
        response, courier_data = courier_response
        duplicate_response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=courier_data)
        assert duplicate_response.status_code == 409 and duplicate_response.json().get('message') == "Этот логин уже используется"
