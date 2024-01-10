import requests
from helpers import BASE_URL, LOGIN_COURIER_ENDPOINT
import allure
from conftest import courier_response


class TestCourierLogin:


    @allure.title("Успешный вход курьера и получение ID")
    @allure.description("Проверка успешного входа в систему курьера и получения его уникального ID")
    def test_courier_login_success_and_return_id(self, courier_response):
        _, courier_data = courier_response
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login'], "password": courier_data['password']}
        )
        assert response.status_code == 200 and "id" in response.json()
        print(response.text)


    @allure.title("Вход курьера без указания пароля")
    @allure.description("Проверка ошибки при попытке входа без указания логина")
    def test_courier_login_missing_field(self, courier_response):
        _, courier_data = courier_response
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"password": courier_data['password']}
        )
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для входа"
        print(response.text)


    @allure.title("Вход курьера без указания логина")
    @allure.description("Проверка ошибки при попытке входа без указания пароля")
    def test_courier_password_missing_field(self, courier_response):
        _, courier_data = courier_response
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login']}
        )
        assert response.status_code == 400 and response.json()['message'] == "Недостаточно данных для входа"
        print(response.text)


    @allure.title("Вход курьера с неверным паролем")
    @allure.description("Проверка ошибки при входе с неправильным паролем")
    def test_courier_login_wrong_password(self, courier_response):
        _, courier_data = courier_response
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": courier_data['login'], "password": "wrong_password"}
        )
        assert response.status_code == 404 and response.json()['message'] == "Учетная запись не найдена"
        print(response.text)


    @allure.title("Вход несуществующего курьера")
    @allure.description("Проверка ошибки при попытке входа с данными несуществующего пользователя")
    def test_courier_login_nonexistent_user(self, courier_response):
        _, courier_data = courier_response
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": "nonexistentuser", "password": courier_data['password']}
        )
        assert response.status_code == 404 and response.json()['message'] == "Учетная запись не найдена"
        print(response.text)


