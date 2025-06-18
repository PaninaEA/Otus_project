import allure
import pytest

from api_services.entities_api import EntitiesApi


@pytest.fixture(scope="module")
def api():
    return EntitiesApi()


@pytest.fixture()
def entity_data() -> dict:
    return {
        "type_station": [
            "StationType",
            "NtGRES",
            "00000000-0000-0000-0003-000000005007",
        ],
        "type_blok": ["BlockType", "PGU1", "00000000-0000-0000-0003-000000005016"],
        "type_raw_var": [
            "ParameterRawVarType",
            "Pset",
            "00000000-0000-0000-0003-000000006045",
        ],
        "type_proc_var": [
            "ParameterProcVarType",
            "Freq1",
            "00000000-0000-0000-0003-000000006043",
        ],
    }


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity property")
@pytest.mark.parametrize(
    "entity_type, count",
    [
        ("type_station", 1),
        ("type_blok", 8),
        ("type_raw_var", 0),
    ],
)
def test_entity_property(api, entity_data, entity_type, count):
    entity_properties = api.get_entity_property(entity_data[entity_type][2])
    assert len(entity_properties) == count


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity parent")
@pytest.mark.parametrize(
    "entity_type, parent_name",
    [
        ("type_blok", "NtGRES"),
        ("type_raw_var", "PGU1"),
        ("type_station", "Stations"),
    ],
)
def test_entity_parent(api, entity_data, entity_type, parent_name):
    entity_parent = api.get_entity_parent(
        entity_data[entity_type][2], entity_data[entity_type][0]
    )
    assert entity_parent["name"] == parent_name


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity by GUID")
@pytest.mark.parametrize(
    "entity_type", ["type_blok", "type_raw_var", "type_proc_var", "type_raw_var"]
)
def test_entity_by_quid(api, entity_data, entity_type):
    entity = api.get_entity_guid(entity_data[entity_type][2])
    assert entity["Name"] == entity_data[entity_type][1]


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity by name")
@pytest.mark.parametrize(
    "entity_type",
    [
        "type_blok",
        "type_station",
    ],
)
def test_entity_by_name(api, entity_data, entity_type):
    entity = api.get_entity_name(entity_data[entity_type][1])
    assert entity["Id"] == entity_data[entity_type][2]


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity childs")
@pytest.mark.parametrize(
    "entity_type",
    [
        "type_blok",
        "type_station",
    ],
)
def test_entity_childs(api, entity_data, entity_type):
    entity_childs = api.get_entity_childs(entity_data[entity_type][2])
    assert len(entity_childs) >= 1


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Import model")
def test_import_model(api, model_path):
    import_model = api.import_model(model_path)
    assert import_model == 200


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Export model")
def test_export_model(api):
    export_model = api.export_model()
    assert export_model["name"] == "modelExport.xml"


@allure.feature("API methods")
@allure.story("Entities")
@allure.title("Get entity all properties")
@pytest.mark.parametrize(
    "entity_type", ["type_blok", "type_raw_var", "type_proc_var", "type_raw_var"]
)
def test_entity_properties(api, entity_data, entity_type):
    entity = api.get_entity_properties(entity_data[entity_type][2])
    assert entity["Attrs"]["Id"] == entity_data[entity_type][2]
    assert entity["Attrs"]["Name"] == entity_data[entity_type][1]
