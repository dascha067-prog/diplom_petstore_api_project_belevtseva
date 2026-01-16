import allure
import pytest

from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


@allure.epic("Petstore API")
@allure.feature("User")
@allure.tag("api")
@allure.label("owner", "Belevtseva Darya")
@pytest.mark.api
class TestGetUser:

    @allure.story("Получение пользователя")
    @allure.title("Успешное получение пользователя по username")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_existing_user(self, api_client):
        username = VALID_USER_DATA["username"]
        allure.dynamic.parameter("username", username)
        api_client.create_user(VALID_USER_DATA)

        response, result = api_client.get_user(username)

        with allure.step("Проверка, что возвращается статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверка, что username соответствует ожидаемому"):
            assert result["username"] == username

        with allure.step("Проверка схемы ответа через Pydantic"):
            User.model_validate(result)

    @allure.story("Получение пользователя")
    @allure.title("Получение несуществующего пользователя возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_nonexistent_user(self, api_client):
        username = INVALID_USER_DATA[-1]["username"]
        allure.dynamic.parameter("username", username)

        response, result = api_client.get_user(username)

        with allure.step("Проверка, что возвращается статус код 404"):
            assert response.status_code == 404

        with allure.step("Проверка структуры ошибки через Pydantic"):
            ErrorResponse.model_validate(result)
