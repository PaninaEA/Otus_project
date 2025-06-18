import allure
import pytest

from page_objects.model_page import ModelPage


@pytest.fixture()
def new_property() -> dict:
    return {
        "Код": "test",
        "Наименование": "Тестовое свойство",
        "Значение": "test",
    }


@allure.feature("Find elements")
@allure.story("Model page")
@allure.title("Elements on model page")
def test_find_elements(page, site_url, usr_login):
    ModelPage(page).open_model_page(site_url, usr_login)
    ModelPage(page).model_page_data_grid()
    ModelPage(page).model_page_buttons()


@allure.feature("Check import function")
@allure.story("Model page")
@allure.title("Import station model")
def test_import_model_page(page, site_url, usr_login, model_path, get_model):
    ModelPage(page).open_model_page(site_url, usr_login)
    print(model_path)
    ModelPage(page).model_page_import(model_path, get_model)


@allure.feature("Check search function")
@allure.story("Model page")
@allure.title("Search on model page")
@pytest.mark.parametrize("search_text", ["пгу", "ГРЭС"])
def test_search_model_page(page, site_url, usr_login, search_text):
    ModelPage(page).open_model_page(site_url, usr_login)
    ModelPage(page).model_page_search(search_text)


@allure.feature("Find elements")
@allure.story("Model page")
@allure.title("Parameters of entity on model page")
def test_model_parameters(page, site_url, usr_login):
    ModelPage(page).open_model_page(site_url, usr_login)
    ModelPage(page).select_entity()
    ModelPage(page).entity_property()
    ModelPage(page).entity_attribute()


@allure.feature("Check update function")
@allure.story("Model page")
@allure.title("Property data update on model page")
def test_model_property_data_update(page, site_url, usr_login):
    ModelPage(page).open_model_page(site_url, usr_login)
    ModelPage(page).select_entity()
    ModelPage(page).entity_property_data_update()


@allure.feature("Check update function")
@allure.story("Model page")
@allure.title("Property changes on model page")
def test_model_property_changes(page, site_url, usr_login, new_property):
    ModelPage(page).open_model_page(site_url, usr_login)
    ModelPage(page).select_entity()
    ModelPage(page).entity_property_add(new_property)
    ModelPage(page).entity_property_edit(new_property)
    ModelPage(page).entity_property_remove(new_property)
