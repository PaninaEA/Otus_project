from typing import Dict

import allure

from api_services.base_api import APIWrapper


class NsiApi(APIWrapper):
    @allure.step("Получение настроек объекта из НСИ")
    def get_entity_config(self, object_id: str) -> Dict:
        response = self.send_request("GET", "Nsi/getConfig", params={"msg": object_id})
        return response.json()
