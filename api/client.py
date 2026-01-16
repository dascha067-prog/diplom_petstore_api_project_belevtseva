import allure
import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_user(self, user_data: dict):
        url = f"{self.base_url}/user"
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(url, json=user_data)
            self._attach_response(response)
            self._attach_log(response)
        return response, response.json()

    def get_user(self, username: str):
        url = f"{self.base_url}/user/{username}"
        with allure.step("Отправка запроса на получение пользователя"):
            response = requests.get(url)
            self._attach_response(response)
            self._attach_log(response)
        return response, response.json()

    def update_user(self, username: str, update_data: dict):
        url = f"{self.base_url}/user/{username}"
        with allure.step("Отправка запроса на обновление пользователя"):
            response = requests.put(url, json=update_data)
            self._attach_response(response)
            self._attach_log(response)
        return response, response.json()

    def delete_user(self, username: str):
        url = f"{self.base_url}/user/{username}"
        with allure.step("Отправка запроса на удаление пользователя"):
            response = requests.delete(url)
            self._attach_response(response)
            self._attach_log(response)
        return response

    def _attach_response(self, response: requests.Response):
        allure.attach(
            name="Request",
            body=f"{response.request.method} {response.request.url}\n\n{response.request.body}",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            name="Response",
            body=f"Status: {response.status_code}\n\n{response.text}",
            attachment_type=allure.attachment_type.JSON
            if response.headers.get("Content-Type", "").startswith("application/json")
            else allure.attachment_type.TEXT
        )

    def _attach_log(self, response: requests.Response):
        req = response.request
        log_text = (
            f"INFO Request: {req.method} {req.url}\n"
            f"INFO Request body: {req.body}\n"
            f"INFO Response code: {response.status_code}\n"
        )
        allure.attach(log_text, name="log", attachment_type=allure.attachment_type.TEXT)
