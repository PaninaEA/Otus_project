import allure
from playwright.sync_api import expect

from page_objects.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Открытие главной страницы")
    def open_main_page(self, url, login):
        self.open_site(url)
        self.login(login)

    @allure.step("Проверка авторизации")
    def check_authorization(self, login):
        expect(
            self.page.locator("div.mainHeader__user>i.dx-icon-user"),
            f"Ошибка авторизации для {login}",
        ).to_contain_text(login)

    @allure.step("Выход из аккаунта")
    def logout(self):
        self.page.get_by_role("button", name="export").click()
        expect(
            self.page.get_by_role("heading", name="Войдите в аккаунт"),
            "Ошибка выхода из аккаунта",
        ).to_be_visible()

    @allure.step("Проверка название страницы")
    def title(self):
        return self.page.title()

    @allure.step("Проверка логотипа на странице")
    def logo(self):
        self.page.get_by_role("img", name="ПРОСТОР")

    @allure.step("Проверка футера на странице")
    def footer(self, site_version):
        self.page.get_by_text("©ПРОСТОРЛАБ")
        self.page.get_by_text(f"{site_version}")

    @allure.step("Проверка ссылки на сайт prostorlab.com")
    def link(self):
        with self.page.expect_popup() as link_page:
            self.page.get_by_role("link", name="prostorlab.com").click()
        page_prostor = link_page.value
        page_prostor.get_by_role("heading", name="Платформа Простор")
        page_prostor.close()

    @allure.step("Проверка пунктов главного меню")
    def main_menu_items(self):
        self.page.wait_for_selector("div.mainHeader__navigation")
        return self.page.locator("div.mainHeader__navigation>a").all()
