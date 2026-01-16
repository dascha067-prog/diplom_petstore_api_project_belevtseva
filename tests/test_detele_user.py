import pytest
from api.schemas import ErrorResponse, User
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


class TestDeleteUser:
    @pytest.mark.positive
    def test_delete_existing_user(self, api_client):
        api_client.create_user(VALID_USER_DATA)

        delete_response = api_client.delete_user(VALID_USER_DATA["username"])
        assert delete_response.status_code == 200

        # Проверяем, что пользователь реально удалён
        get_response, _ = api_client.get_user(VALID_USER_DATA["username"])
        assert get_response.status_code == 404

    @pytest.mark.negative
    def test_delete_nonexistent_user(self, api_client):
        # Пытаемся удалить несуществующего пользователя
        response = api_client.delete_user(INVALID_USER_DATA)

        # Проверяем, что сервер вернёт 404
        assert response.status_code == 404