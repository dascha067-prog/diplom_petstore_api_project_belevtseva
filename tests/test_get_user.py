import pytest
from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


class TestGetUser:

    @pytest.mark.positive
    def test_get_existing_user(self, api_client):
        # Act — создаём пользователя и получаем его по username
        api_client.create_user(VALID_USER_DATA)
        response, result = api_client.get_user(VALID_USER_DATA["username"])

        # Assert — проверяем успешный ответ
        assert response.status_code == 200
        assert result["username"] == VALID_USER_DATA["username"]

        # Валидация через Pydantic
        User.model_validate(result)

    @pytest.mark.negative
    def test_get_nonexistent_user (self, api_client):
        # Act — запрашиваем несуществующего пользователя
        response, result = api_client.get_user(INVALID_USER_DATA)

        # Проверка кода
        assert response.status_code == 404

        # Проверка структуры ошибки через Pydantic
        error = ErrorResponse.model_validate(result)

        # Валидация через Pydantic
        ErrorResponse.model_validate(result)
