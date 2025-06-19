import allure
import pytest

from page_objects.main_page import MainPage


@allure.feature("Check site access")
@allure.story("Main page")
@allure.title("Open main page")
def test_login(page, site_url, usr_login):
    MainPage(page).open_main_page(site_url, usr_login)
    MainPage(page).check_authorization(usr_login)


@allure.feature("Check site access")
@allure.story("Main page")
@allure.title("Logout on main page")
def test_logout(page, site_url, usr_login):
    MainPage(page).open_main_page(site_url, usr_login)
    MainPage(page).logout()


@allure.feature("Find elements")
@allure.story("Main page")
@allure.title("Elements on main page")
def test_find_elements(page, site_url, usr_login, site_version):
    MainPage(page).open_main_page(site_url, usr_login)
    MainPage(page).logo()
    MainPage(page).footer(site_version)
    MainPage(page).link()
    assert MainPage(page).title() == "ПРОСТОР"


@allure.feature("Find elements")
@allure.story("Main page")
@allure.title("Items in main menu")
@pytest.mark.parametrize(
    "login, items_count",
    [("Admin", 5), ("User", 4), ("ViewOnly", 1)],
)
def test_main_menu(page, site_url, login, items_count):
    MainPage(page).open_main_page(site_url, login)
    MainPage(page).check_authorization(login)
    assert len(MainPage(page).main_menu_items()) == items_count
