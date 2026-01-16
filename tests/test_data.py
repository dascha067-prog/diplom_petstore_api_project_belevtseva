from api.schemas import User

VALID_USER_DATA = User(
    id=101,
    username="daria_test",
    firstName="Дарья",
    lastName="Иванова",
    email="daria@example.com",
    password="12345",
    phone="89991234567",
    userStatus=1,
).model_dump()

INVALID_USER_DATA = [
    {"username": "", "email": "daria@example.com", "userStatus": 1},  # Пустой username
    {"username": "daria", "email": "not-an-email", "userStatus": 1},  # Невалидный email
    {"username": "daria", "email": "daria@example.com", "userStatus": -5},  # Некорректный userStatus
    {"username": "daria", "email": "daria@example.com"},  # Отсутствуют обязательные поля
    {"username": "daria", "email": "daria@example.com", "password": "", "userStatus": 1},  # Пустой пароль
    {"username": "daria", "email": "daria@example.com", "phone": "12345", "userStatus": 1},  # Неправильный формат номера телефона (длина, формат)
    {"username": "daria", "email": "daria@example.com", "firstName": None, "userStatus": 1},  # None в обязательном поле
    {"username": "nonexistent_user_123"},  # Несуществующий пользователь для тестов get/delete
]