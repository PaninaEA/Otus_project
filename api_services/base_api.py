from typing import Dict, Optional, Any

import allure
import requests


class APIWrapper:
    def __init__(self):
        self.base_url = "http://vm-prostor-qa:30000/v4/StationModels/"

    @allure.step("Получение url")
    def get_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    @property
    @allure.step("Получение headers")
    def get_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def send_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self.get_url(path)
        headers = headers if headers is not None else self.get_headers
        with allure.step(f"Отправка {method} запроса на {path}"):
            response = requests.request(
                method=method, url=url, headers=headers, params=params, data=data
            )
        return response
