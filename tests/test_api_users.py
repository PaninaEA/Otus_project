import random

import allure
import pytest
from faker import Faker
from random_username.generate import generate_username

from api_services.user_api import UsersApi


@pytest.fixture(scope="module")
def api():
    return UsersApi()


@pytest.fixture()
def create_user(role, parent) -> dict:
    fake = Faker("ru_RU")
    return {
        "Fullname": fake.name(),
        "Login": generate_username()[0],
        "Email": fake.email(),
        "Password": fake.password(),
        "Role": role,
        "Inactive": 0,
        "Node": 10001,
        "ParentId": parent,
    }


@pytest.fixture()
def user_viewonly(api) -> dict:
    return api.get_user_data("ViewOnly")


@pytest.fixture()
def updated_data(api) -> dict:
    updated_user = api.get_user_data("ViewOnly")
    updated_user["Login"] = "ViewOnly_test"
    return updated_user


@pytest.fixture()
def data_login() -> dict:
    return {
        "role_admin": {
            "Id": "00000000-0000-0000-0000-000000010001",
            "Value": "Admintest",
        },
        "role_user": {
            "Id": "00000000-0000-0000-0000-000000010002",
            "Value": "User_test",
        },
        "role_view": {
            "Id": "00000000-0000-0000-0000-000000010003",
            "Value": "ViewOnlyvalidate123",
        },
    }


@pytest.fixture()
def data_email() -> dict:
    return {
        "role_admin": {
            "Id": "00000000-0000-0000-0000-000000010001",
            "Value": "Admintest@prostor.ru",
        },
        "role_user": {
            "Id": "00000000-0000-0000-0000-000000010002",
            "Value": "User_test@prostor.ru",
        },
        "role_view": {
            "Id": "00000000-0000-0000-0000-000000010003",
            "Value": "ViewOnlyvalidate123@prostor.ru",
        },
    }


@pytest.fixture()
def data_invalid(role) -> dict:
    return {
        "role_admin": {
            "Id": "00000000-0000-0000-0000-000000010001",
            "Value": random.randint(10000, 50000),
        },
        "role_user": {"Id": "00000000-0000-0000-0000-000000010002", "Value": None},
    }


@allure.feature("API methods")
@allure.story("Users")
@allure.title("Get list of users")
def test_list_of_users(api):
    users = api.get_list_of_users()
    assert len(users) > 1


@allure.feature("API methods")
@allure.story("Users")
@allure.title("Get role for user")
@pytest.mark.parametrize(
    "login, role",
    [("Admin", 1), ("User", 2), ("ViewOnly", 3)],
)
def test_user(api, login, role):
    user = api.get_user_data(login)
    assert user["Role"] == role


@allure.feature("API methods")
@allure.story("Users")
@allure.title("Update user")
def test_update_user(api, user_viewonly, updated_data):
    api.edit_user(updated_data)
    user_updated = api.get_user_data(updated_data["Login"])
    assert user_updated == updated_data
    api.edit_user(user_viewonly)


@allure.feature("API methods")
@allure.story("Users")
@allure.title("Validate positive")
@pytest.mark.parametrize(
    "role",
    ["role_admin", "role_user", "role_view"],
)
def test_validate_positive(api, role, data_login, data_email):
    assert api.validate_login(data_login[role])
    assert api.validate_email(data_email[role])


@allure.feature("API methods")
@allure.story("Users")
@allure.title("Validate negative")
@pytest.mark.parametrize(
    "role",
    [
        "role_admin",
        "role_user",
    ],
)
def test_validate_negative(api, role, data_invalid):
    assert api.validate_login(data_invalid[role])["status"] == 400
    assert api.validate_email(data_invalid[role])["status"] == 400
