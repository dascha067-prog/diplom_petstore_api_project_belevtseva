# conftest.py
import allure
import pytest
from api.client import ApiClient

@pytest.fixture(scope="function")
def api_client():
    with allure.step("Инициализация API клиента"):
        return ApiClient(base_url="https://petstore.swagger.io/v2")
