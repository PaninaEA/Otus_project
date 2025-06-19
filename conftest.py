from pathlib import Path

from dotenv import load_dotenv
import os
import allure
from playwright.sync_api import sync_playwright
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--site_version", type=str, default="4.1.0", help="Prostor version"
    )
    parser.addoption(
        "--browser_name", type=str, default="chrome", help="Browser for tests"
    )  # msedge,
    parser.addoption(
        "--url", type=str, default="https://vm-prostor-qa", help="Url for site"
    )
    parser.addoption("--headless", action="store_true", default=True)
    parser.addoption(
        "--login", type=str, default="Admin", help="Login for authorization"
    )
    parser.addoption(
        "--model:name",
        type=str,
        default="ntgres_dev:Нижнетуринская",
        help="Файл модели:наименование станции",
    )


@pytest.fixture()
def page(request):
    browser_name = request.config.getoption("--browser_name")
    headless = request.config.getoption("--headless")
    with sync_playwright() as play:
        browser = play.chromium.launch(
            channel=browser_name,
            headless=headless,
            args=[
                "--start-maximized",
                "--disable-web-security",
                "--ignore-certificate-errors",
            ],
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture
def usr_login(request):
    return request.config.getoption("--login")


def logins_pwd(login):
    load_dotenv()
    pwd = os.environ.get(f"secret{login}")
    return pwd


@pytest.fixture
def site_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def site_version(request):
    return request.config.getoption("--site_version")


@pytest.fixture
def get_model(request):
    return request.config.getoption("--model:name")


@pytest.fixture
def model_path(get_model) -> str:
    tests_dir = Path(__file__).parent
    xml_path = f"{tests_dir}/{get_model.split(':')[0]}.xml"
    return xml_path


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            allure.attach(
                page.screenshot(),
                name=item.name,
                attachment_type=allure.attachment_type.PNG,
            )
