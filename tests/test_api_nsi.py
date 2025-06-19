import allure
import pytest

from api_services.nsi_api import NsiApi


@pytest.fixture(scope="module")
def api():
    return NsiApi()


@allure.feature("API methods")
@allure.story("Nsi")
@allure.title("Get entity config")
@pytest.mark.parametrize(
    "id_object",
    [
        "00000000-0000-0000-0003-000000005016",
        "00000000-0000-0000-0003-000000006001",
        "00000000-0000-0000-0003-000000006043",
    ],
)
def test_entity_config(api, id_object):
    entity = api.get_entity_config(id_object)
    assert len(entity) > 1
