from typing import Dict

import allure

from api_services.base_api import APIWrapper


class EntitiesApi(APIWrapper):
    @allure.step("Получение свойств объекта")
    def get_entity_property(self, entity_id) -> Dict:
        response = self.send_request(
            "GET", "Entities/getEntityProperty", params={"entityId": entity_id}
        )
        return response.json()

    @allure.step("Получение родительского объекта")
    def get_entity_parent(self, entity_id, type_name) -> Dict:
        response = self.send_request(
            "GET",
            "Entities/getEntityParent",
            params={"entityId": entity_id, "typeName": type_name},
        )
        return response.json()

    @allure.step("Получение объекта по GUID")
    def get_entity_guid(self, entity_id) -> Dict:
        response = self.send_request(
            "GET", "Entities/getEntity", params={"entityId": entity_id}
        )
        return response.json()

    @allure.step("Получение объекта по наименованию")
    def get_entity_name(self, entity_name) -> Dict:
        response = self.send_request(
            "GET", "Entities/getEntityName", params={"entityName": entity_name}
        )
        return response.json()

    @allure.step("Получение дочерних объектов")
    def get_entity_childs(self, entity_id) -> Dict:
        response = self.send_request(
            "GET", "Entities/getEntityChilds", params={"entityId": entity_id}
        )
        return response.json()

    @allure.step("Импорт модели")
    def import_model(self, file_path):
        with open(file_path, "rb") as f:
            response = self.send_request(
                "POST", "Entities/import", headers={"Content-Type": "text/xml"}, data=f
            )
        return response.status_code

    @allure.step("Экспорт модели")
    def export_model(self):
        response = self.send_request(
            "GET", "Entities/export", params={"ids": "%27%20%27"}
        )
        return response.json()

    @allure.step("Получение всех параметров объекта")
    def get_entity_properties(self, entity_id) -> Dict:
        response = self.send_request(
            "GET", "Entities/getEntityProperties", params={"entityId": entity_id}
        )
        return response.json()
