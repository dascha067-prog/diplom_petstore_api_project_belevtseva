import pytest
from api.client import ApiClient

@pytest.fixture(scope="session")
def api_client():
    return ApiClient(base_url="https://petstore.swagger.io/v2")