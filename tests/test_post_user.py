import pytest
from api.schemas import User, ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


# КОРОТКИЙ ТЕСТ С ИСПОЛЬЗОВАНИЕМ ВСЕЙ СТРУКТУРЫ ПРОЕКТА – ФИКСТУРЫ И ВАЛИДАЦИИ СХЕМ


class TestCreateUser:
    @pytest.mark.positive
    def test_create_valid_user(self, api_client):
        # Создаём пользователя
        post_response, _ = api_client.create_user(VALID_USER_DATA)
        assert post_response.status_code == 200

        # Делаем GET-запрос, чтобы получить созданного пользователя
        get_response, user_data = api_client.get_user(VALID_USER_DATA["username"])
        assert get_response.status_code == 200

        # Проверяем данные
        assert user_data["username"] == VALID_USER_DATA["username"]

        # Валидация через Pydantic
        User.model_validate(user_data)

    @pytest.mark.negative
    @pytest.mark.xfail(reason="Бэк не валидирует пустой username — ожидается 400, но приходит 200", strict=True)
    def test_create_user_with_empty_username(self, api_client):
            # Act – пытаемся создать пользователя с пустым username
            response, result = api_client.create_user(INVALID_USER_DATA[0])

            # Assert – проверяем, что сервер должен возвращать ошибку (пока возвращает 200 — это баг)
            assert response.status_code == 400

            # Проверка, что в ответе действительно есть ошибка
            assert "errors" in result, "Ожидалась структура с ошибками"

            # Валидация через Pydantic
            ErrorResponse.model_validate(result)