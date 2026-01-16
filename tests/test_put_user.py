import allure
import pytest

from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


@allure.epic("Petstore API")
@allure.feature("User")
@allure.tag("api")
@allure.label("owner", "Belevtseva Darya")
@pytest.mark.api
class TestUpdateUser:

    @allure.story("Обновление пользователя")
    @allure.title("Успешное обновление данных пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_update_user(self, api_client):
        username = VALID_USER_DATA["username"]
        allure.dynamic.parameter("username", username)

        with allure.step("Создать пользователя"):
            post_response, _ = api_client.create_user(VALID_USER_DATA)
            assert post_response.status_code == 200

        with allure.step("Подготовить данные для обновления пользователя"):
            updated_data = VALID_USER_DATA.copy()
            updated_data["firstName"] = "UpdatedName"

        with allure.step("Отправить запрос на обновление пользователя"):
            put_response, _ = api_client.update_user(username, updated_data)

        with allure.step("Проверка, что возвращается статус код 200"):
            assert put_response.status_code == 200

        with allure.step("Получить пользователя и проверить обновлённые данные"):
            get_response, user_data = api_client.get_user(username)
            assert get_response.status_code == 200
            assert user_data["firstName"] == "UpdatedName"

        with allure.step("Проверка схемы ответа через Pydantic"):
            User.model_validate(user_data)

    @allure.story("Обновление пользователя")
    @allure.title("Обновление пользователя с некорректным email возвращает ошибку")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="API не валидирует некорректный email: ожидается 400, но приходит 200",
        strict=True
    )
    def test_update_user_with_invalid_email(self, api_client):
        username = VALID_USER_DATA["username"]
        allure.dynamic.parameter("username", username)

        with allure.step("Создать пользователя"):
            post_response, _ = api_client.create_user(VALID_USER_DATA)
            assert post_response.status_code == 200

        with allure.step("Подготовить данные с некорректным email"):
            invalid_data = VALID_USER_DATA.copy()
            invalid_data["email"] = "not-an-email"

        with allure.step("Отправить запрос на обновление пользователя с некорректным email"):
            response, result = api_client.update_user(username, invalid_data)

        with allure.step("Проверка, что возвращается статус код 400"):
            assert response.status_code == 400

        with allure.step("Проверка структуры ошибки через Pydantic"):
            ErrorResponse.model_validate(result)
