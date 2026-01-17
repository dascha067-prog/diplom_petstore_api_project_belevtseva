import allure
import pytest

from api.schemas import ErrorResponse
from tests.test_data import VALID_USER_DATA, INVALID_USER_DATA


@allure.epic("Petstore API")
@allure.feature("User")
@allure.label("layer", "api")
@allure.tag("api")
@allure.label("owner", "Belevtseva Darya")
@pytest.mark.api
class TestDeleteUser:

    @allure.story("Удаление пользователя")
    @allure.title("Успешное удаление существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_delete_existing_user(self, api_client):
        username = VALID_USER_DATA["username"]
        allure.dynamic.parameter("username", username)

        with allure.step("Создать пользователя"):
            response, _ = api_client.create_user(VALID_USER_DATA)
            assert response.status_code == 200

        with allure.step("Удалить пользователя по username"):
            delete_response = api_client.delete_user(username)

        with allure.step("Проверка, что возвращается статус код 200"):
            assert delete_response.status_code == 200

        with allure.step("Проверить, что пользователь действительно удалён (GET возвращает 404)"):
            get_response, result = api_client.get_user(username)
            assert get_response.status_code == 404

        with allure.step("Проверка структуры ошибки через Pydantic"):
            ErrorResponse.model_validate(result)

    @allure.story("Удаление пользователя")
    @allure.title("Удаление несуществующего пользователя возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_delete_nonexistent_user(self, api_client):
        # Берём username из последнего элемента списка (как ты уже делала в test_data.py)
        username = INVALID_USER_DATA[-1]["username"]
        allure.dynamic.parameter("username", username)

        with allure.step("Удалить несуществующего пользователя по username"):
            response = api_client.delete_user(username)

        with allure.step("Проверка, что возвращается статус код 404"):
            assert response.status_code == 404
