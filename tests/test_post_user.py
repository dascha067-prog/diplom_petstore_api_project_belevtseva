import allure
import pytest

from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


@allure.epic("Petstore API")
@allure.feature("User")
@allure.tag("api")
@allure.label("owner", "Belevtseva Darya")
@pytest.mark.api
class TestCreateUser:

    @allure.story("Создание пользователя")
    @allure.title("Успешное создание пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_create_valid_user(self, api_client):
        username = VALID_USER_DATA["username"]
        allure.dynamic.parameter("username", username)

        with allure.step("Отправить запрос на создание пользователя"):
            post_response, _ = api_client.create_user(VALID_USER_DATA)

        with allure.step("Проверка, что возвращается статус код 200"):
            assert post_response.status_code == 200

        with allure.step("Получить созданного пользователя по username"):
            get_response, user_data = api_client.get_user(username)

        with allure.step("Проверка, что возвращается статус код 200"):
            assert get_response.status_code == 200

        with allure.step("Проверка, что данные пользователя совпадают с ожидаемыми"):
            assert user_data["username"] == username

        with allure.step("Проверка схемы ответа через Pydantic"):
            User.model_validate(user_data)

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя с пустым username возвращает ошибку")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="API не валидирует пустой username: ожидается 400, но приходит 200",
        strict=True
    )
    def test_create_user_with_empty_username(self, api_client):
        invalid_data = INVALID_USER_DATA[0]
        allure.dynamic.parameter("username", invalid_data.get("username"))

        with allure.step("Отправить запрос на создание пользователя с пустым username"):
            response, result = api_client.create_user(invalid_data)

        with allure.step("Проверка, что возвращается статус код 400"):
            assert response.status_code == 400

        with allure.step("Проверка структуры ошибки через Pydantic"):
            ErrorResponse.model_validate(result)
