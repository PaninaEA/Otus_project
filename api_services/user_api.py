import json
from typing import Dict

import allure

from api_services.base_api import APIWrapper


class UsersApi(APIWrapper):
    @allure.step("Получение списка пользователей")
    def get_list_of_users(self) -> Dict:
        response = self.send_request("GET", "Users/getUsers")
        return response.json()

    @allure.step("Получение данных пользователя {login}")
    def get_user_data(self, login: str) -> Dict:
        response = self.send_request("GET", "Users/getUser", params={"login": login})
        return response.json()

    @allure.step("Редактирование пользователя")
    def edit_user(self, user):
        response = self.send_request("PUT", "Users/updateUser", data=json.dumps(user))
        return response.status_code

    @allure.step("Валидация логина для {user}")
    def validate_login(self, user) -> Dict:
        response = self.send_request(
            "POST", "Users/validateLogin", data=json.dumps(user)
        )
        return response.json()

    @allure.step("Валидация email для {user}")
    def validate_email(self, user) -> Dict:
        response = self.send_request(
            "POST", "Users/validateEmail", data=json.dumps(user)
        )
        return response.json()
