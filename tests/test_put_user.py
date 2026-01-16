import pytest
from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


class TestUpdateUser:

    @pytest.mark.positive
    def test_update_user(self, api_client):
        # Arrange — создаём пользователя
        post_response, _ = api_client.create_user(VALID_USER_DATA)
        assert post_response.status_code == 200

        # Act — обновляем пользователя
        updated_data = VALID_USER_DATA.copy()
        updated_data["firstName"] = "UpdatedName"
        put_response, _ = api_client.update_user(updated_data["username"], updated_data)
        assert put_response.status_code == 200

        # Assert — получаем и проверяем обновлённые данные
        get_response, user_data = api_client.get_user(updated_data["username"])
        assert get_response.status_code == 200
        assert user_data["firstName"] == "UpdatedName"

        # Валидация через Pydantic
        User.model_validate(user_data)

    @pytest.mark.negative  # Тест на некорректные данные (невалидный email)
    @pytest.mark.xfail(reason="Бэк не валидирует некорректный email — ожидается 400, но приходит 200", strict=True)
    def test_update_user_with_invalid_email(self, api_client):
        # Act — пытаемся обновить пользователя с невалидным email
        invalid_data = INVALID_USER_DATA[1]
        response, result = api_client.update_user(invalid_data["username"], invalid_data)

        # Assert — проверяем, что сервер должен возвращать ошибку (ожидается 400)
        assert response.status_code == 400

        # Проверка, что в ответе есть информация об ошибке
        assert "errors" in result, "Ожидалась структура с ошибками"

        # Валидация через Pydantic
        ErrorResponse.model_validate(result)
