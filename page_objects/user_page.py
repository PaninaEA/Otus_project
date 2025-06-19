import allure
from playwright.sync_api import expect

from page_objects.base_page import BasePage


class UserPage(BasePage):
    @allure.step("Открытие страницы Пользователи")
    def open_user_page(self, url, login):
        self.open_site(url)
        self.login(login)
        self.page.get_by_role("link", name="Пользователи").click()

    @allure.step("Проверка дерева пользователей")
    def users_tree(self):
        self.page.get_by_text("Администратор").locator("..").locator("div>div").click()
        self.page.get_by_label("Tree list", exact=True).get_by_text("Admin")
        self.page.get_by_text("Пользователь").locator("..").locator("div>div").click()
        self.page.get_by_label("Tree list", exact=True).get_by_text("User")
        self.page.get_by_text("Только просмотр").locator("..").locator(
            "div>div"
        ).click()
        self.page.get_by_label("Tree list", exact=True).get_by_text("ViewOnly")

    @allure.step("Проверка поиска")
    def search(self, search_text):
        self.page.get_by_role("textbox", name="Search in the tree list").click()
        self.page.get_by_role("textbox", name="Search in the tree list").fill(
            search_text
        )
        expect(self.page.locator("span.dx-treelist-search-text")).to_have_text(
            search_text, ignore_case=True
        )

    @allure.step("Проверка доступности кнопки сохранения")
    def button_save(self):
        save_button_stat = self.page.get_by_role("button", name="save").get_attribute(
            "tabindex"
        )
        return save_button_stat

    @allure.step("Проверка доступности кнопки добавления")
    def button_add(self):
        add_button_stat = self.page.get_by_role("button", name="add").get_attribute(
            "tabindex"
        )
        return add_button_stat

    @allure.step("Проверка отображения таблицы")
    def data_grid(self):
        expect(
            self.page.get_by_label("Data grid").get_by_label("Column Наименование")
        ).to_contain_text("Наименование")
        expect(
            self.page.get_by_label("Data grid").get_by_label("Column Значение")
        ).to_contain_text("Значение")
        expect(self.page.get_by_label("Data grid")).to_contain_text("No data")

    @allure.step("Проверка отображения параметров пользователя")
    def user_property(self):
        self.page.get_by_text("Пользователь").locator("..").locator("div>div").click()
        self.page.locator("//tr[@role='row' and @aria-level='2']").click()
        user_login = self.page.locator("tr[aria-selected='true']").text_content()
        self.page.get_by_role("Gridcell", name="Email")
        self.page.get_by_role("Gridcell", name="Fullname")
        self.page.get_by_role("Gridcell", name="Inactive")
        self.page.get_by_role("Gridcell", name="Login")
        self.page.get_by_role("Gridcell", name="Password")
        self.page.get_by_role("button", name="Изменить пароль")
        self.page.get_by_role("Gridcell", name="Role")
        expect(self.page.get_by_role("combobox")).to_have_value("Пользователь")
        expect(
            self.page.get_by_role("row", name="Login").get_by_role("textbox")
        ).to_have_value(user_login)
        expect(self.page.get_by_role("tab", name="Свойства")).to_have_attribute(
            "aria-selected", "true"
        )

    @allure.step("Изменение и сохранение значения поля")
    def textbox_update(self, role_name, text):
        self.page.get_by_role("row", name=role_name).get_by_role("textbox").fill(text)
        self.page.get_by_role("row", name=role_name).get_by_role("textbox").press(
            "Enter"
        )
        self.page.get_by_role("button", name="save").click()

    @allure.step("Проверка изменения параметров пользователя")
    def user_property_update(self):
        self.page.get_by_text("Только просмотр").locator("..").locator(
            "div>div"
        ).click()
        self.page.locator("//tr[@role='row' and @aria-level='2']").click()
        current_text = (
            self.page.get_by_role("row", name="Fullname")
            .get_by_role("textbox")
            .input_value()
        )
        self.textbox_update("Fullname", f"{current_text}test")
        self.page.locator("//tr[@role='row' and @aria-level='2']").click()
        expect(
            self.page.get_by_role("row", name="Fullname").get_by_role("textbox")
        ).to_have_value(f"{current_text}test")
        self.textbox_update("Fullname", current_text)
        self.page.locator("//tr[@role='row' and @aria-level='2']").click()
        expect(
            self.page.get_by_role("row", name="Fullname").get_by_role("textbox")
        ).to_have_value(current_text)

    @allure.step("Проверка заполнения полей при добавлении пользователя")
    def new_user_input_data(self):
        self.page.get_by_label("Tree list", exact=True).get_by_text(
            "Только просмотр"
        ).click()
        self.page.get_by_role("button", name="add").click()
        self.page.get_by_text("Полное имя").locator("..").get_by_role("textbox").fill(
            "Полное имя"
        )
        self.page.get_by_text("Логин").locator("..").get_by_role("textbox").fill(
            "Login"
        )
        self.page.get_by_text("Электронная почта").locator("..").get_by_role(
            "textbox"
        ).fill("test@test.ru")
        self.page.get_by_text("Пароль", exact=True).locator("..").get_by_role(
            "textbox"
        ).fill("Test_1234")
        self.page.get_by_text("Повторите пароль").locator("..").get_by_role(
            "textbox"
        ).fill("Test_1234")
        self.page.get_by_role("radio", name="Только просмотр").click()
        expect(
            self.page.get_by_role("toolbar").filter(
                has_text="Добавление нового пользователя"
            )
        ).to_be_visible()
        expect(self.page.get_by_role("button", name="Сохранить")).to_be_visible()
        self.page.get_by_role("button", name="Отменить").click()
