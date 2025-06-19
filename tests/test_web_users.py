import allure
import pytest

from page_objects.user_page import UserPage


@allure.feature("Find elements")
@allure.story("User page")
@allure.title("Elements on user page")
def test_find_elements(page, site_url, usr_login):
    UserPage(page).open_user_page(site_url, usr_login)
    UserPage(page).users_tree()
    UserPage(page).data_grid()
    assert UserPage(page).button_save() == "-1"
    assert UserPage(page).button_add() == "0"


@allure.feature("Check search function")
@allure.story("User page")
@allure.title("Search on user page")
@pytest.mark.parametrize("search_text", ["Admin", "user", "only"])
def test_search(page, site_url, usr_login, search_text):
    UserPage(page).open_user_page(site_url, usr_login)
    UserPage(page).search(search_text)


@allure.feature("Find elements")
@allure.story("User page")
@allure.title("Property elements on user page")
def test_user_property(page, site_url, usr_login):
    UserPage(page).open_user_page(site_url, usr_login)
    UserPage(page).user_property()


@allure.feature("Check update function")
@allure.story("User page")
@allure.title("Save property changes on user page")
def test_user_property_update(page, site_url, usr_login):
    UserPage(page).open_user_page(site_url, usr_login)
    UserPage(page).user_property_update()


@allure.feature("Check add function")
@allure.story("User page")
@allure.title("Input data for new user")
def test_new_user_input_data(page, site_url, usr_login):
    UserPage(page).open_user_page(site_url, usr_login)
    UserPage(page).new_user_input_data()
