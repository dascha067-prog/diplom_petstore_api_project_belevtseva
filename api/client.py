import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_user(self, user_data: dict) -> tuple[requests.Response, dict]:
        url = f"{self.base_url}/user"
        response = requests.post(url, json=user_data)
        return response, response.json()

    def get_user(self, username: str) -> tuple[requests.Response, dict]:
        url = f"{self.base_url}/user/{username}"
        response = requests.get(url)
        return response, response.json()

    def update_user(self, username: str, update_data: dict) -> tuple[requests.Response, dict]:
        url = f"{self.base_url}/user/{username}"
        response = requests.put(url, json=update_data)
        return response, response.json()

    def delete_user(self, username: str) -> requests.Response:
        url = f"{self.base_url}/user/{username}"
        response = requests.delete(url)
        return response