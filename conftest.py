import pytest
import requests
import random
import string
from data import BASE_URL, DELETE_COURIER_ENDPOINT, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.fixture(scope="function")
def courier_response():
    login = generate_random_string(8)
    password = generate_random_string(8)
    first_name = generate_random_string(8)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=payload)
    courier_id = response.json().get('id')

    response_data = response.json()
    response_data['login'] = login
    response_data['password'] = password
    response_data['firstName'] = first_name

    yield response, response_data

    login_response = requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={"login": login, "password": password}
    )
    courier_id = login_response.json().get('id')
    requests.delete(f"{BASE_URL}{DELETE_COURIER_ENDPOINT}{courier_id}")

