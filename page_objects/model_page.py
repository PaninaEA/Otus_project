import allure
from playwright.sync_api import expect

from page_objects.base_page import BasePage


class ModelPage(BasePage):
    @allure.step("Открытие страницы Модель станции")
    def open_model_page(self, url, login):
        self.open_site(url)
        self.login(login)
        self.page.get_by_role("link", name="Модель станции").click()

    @allure.step("Проверка отображения таблиц")
    def model_page_data_grid(self):
        expect(
            self.page.get_by_label("Tree list", exact=True).get_by_label(
                "Column Наименование"
            )
        ).to_contain_text("Наименование")
        expect(self.page.get_by_role("tab", name="Атрибуты")).to_be_visible()
        expect(self.page.get_by_role("tab", name="Свойства")).to_be_visible()
        expect(self.page.get_by_role("tab", name="Связи")).to_be_visible()
        expect(
            self.page.get_by_role(
                "row", name="Column Наименование Column"
            ).get_by_label("Column Наименование")
        ).to_contain_text("Наименование")
        expect(
            self.page.get_by_role("row").get_by_label("Column Значение")
        ).to_contain_text("Значение")

    @allure.step("Проверка доступности кнопок")
    def model_page_buttons(self):
        expect(self.page.get_by_role("button", name="add")).to_have_attribute(
            "tabindex", "0"
        )
        expect(self.page.get_by_role("button", name="edit")).to_have_attribute(
            "tabindex", "0"
        )
        expect(self.page.get_by_role("button", name="remove")).to_have_attribute(
            "tabindex", "0"
        )
        expect(self.page.get_by_role("button", name="save")).to_have_attribute(
            "tabindex", "-1"
        )
        expect(self.page.get_by_text("↑")).to_be_visible()
        expect(self.page.get_by_text("↓")).to_be_visible()

    @allure.step("Проверка импорта модели")
    def model_page_import(self, model, get_model):
        self.page.locator("input#file-upload").set_input_files(model)
        expect(self.page.get_by_text("Все данные будут стерты")).to_be_visible()
        self.page.get_by_text("Импортировать", exact=True).click()
        expect(self.page.get_by_text("Импорт модели прошел успешно")).to_be_visible()
        self.page.reload()
        expect(self.page.get_by_role("gridcell")).to_contain_text(
            f"{get_model.split(':')[1]}"
        )

    @allure.step("Проверка поиска")
    def model_page_search(self, search_text):
        self.page.get_by_role("textbox").click()
        self.page.get_by_role("textbox").fill(search_text)
        self.page.get_by_role("textbox").press("Enter")
        expect(
            self.page.locator("span.searchSubstring__highlighted").first
        ).to_have_text(search_text, ignore_case=True)

    @allure.step("Выбор объекта модели")
    def select_entity(self):
        self.page.get_by_role("gridcell").locator(
            "div.dx-treelist-icon-container"
        ).first.click()
        self.page.locator("//tr[@role='row' and @aria-level='2']").first.click()

    @allure.step("Проверка отображения свойств объекта")
    def entity_property(self):
        expect(self.page.get_by_role("tab", name="Свойства")).to_have_attribute(
            "aria-selected", "true"
        )
        expect(
            self.page.locator(
                "//tr[@role='row' and @aria-rowindex='1']//input[@class='dx-texteditor-input']"
            )
        ).to_be_visible()

    @allure.step("Проверка отображения атрибутов объекта")
    def entity_attribute(self):
        self.page.get_by_text("Атрибуты").click()
        expect(self.page.get_by_role("gridcell", name="Description")).to_be_visible()
        expect(self.page.get_by_role("gridcell", name="Id", exact=True)).to_be_visible()
        expect(self.page.get_by_role("gridcell", name="Label")).to_be_visible()
        expect(self.page.get_by_role("gridcell", name="NodeIdString")).to_be_visible()
        expect(self.page.get_by_role("gridcell", name="ParentId")).to_be_visible()
        expect(self.page.get_by_role("gridcell", name="Path")).to_be_visible()
        expect(
            self.page.get_by_role("gridcell", name="Type", exact=True)
        ).to_be_visible()

    @allure.step("Изменение и сохранение значения поля")
    def text_edit(self, locator, text):
        self.page.locator(locator).fill(text)
        self.page.locator(locator).press("Enter")
        self.page.get_by_role("button", name="save").click()
        expect(
            self.page.get_by_text("Сохранение свойств прошло успешно")
        ).to_be_visible()

    @allure.step("Проверка изменения значения свойства объекта")
    def entity_property_data_update(self):
        current_value = self.page.locator(
            "//tr[@role='row' and @aria-rowindex='1']//input[@type='text']"
        ).input_value()
        new_value = current_value[:-5] + "43210"
        self.text_edit(
            "//tr[@role='row' and @aria-rowindex='1']//input[@type='text']", new_value
        )
        expect(
            self.page.locator(
                "//tr[@role='row' and @aria-rowindex='1']//input[@type='text']"
            )
        ).to_have_value(new_value)
        self.text_edit(
            "//tr[@role='row' and @aria-rowindex='1']//input[@type='text']",
            current_value,
        )

    @allure.step("Проверка добавления свойств объекта")
    def entity_property_add(self, new_property):
        self.page.locator(
            "//tr[@role='row' and @aria-rowindex='1']//td[@class='cellLabel']"
        ).click()
        self.page.get_by_role("button", name="add").click()
        self.page.get_by_text("Код", exact=True).locator("..").get_by_role(
            "textbox"
        ).fill(new_property["Код"])
        self.page.get_by_text("Наименование", exact=True).locator("..").get_by_role(
            "textbox"
        ).fill(new_property["Наименование"])
        self.page.get_by_text("Значение", exact=True).locator("..").get_by_role(
            "textbox"
        ).fill(new_property["Значение"])
        self.page.get_by_role("button", name="Сохранить").dispatch_event("click")
        expect(
            self.page.get_by_role("gridcell", name=new_property["Наименование"])
        ).to_be_visible()

    @allure.step("Проверка изменения свойств объекта")
    def entity_property_edit(self, new_property):
        self.page.get_by_role("gridcell", name=new_property["Наименование"]).click()
        self.page.get_by_role("button", name="edit").click()
        self.page.get_by_text("Наименование", exact=True).locator("..").get_by_role(
            "textbox"
        ).fill(new_property["Наименование"] + "1")
        self.page.get_by_role("button", name="Сохранить").click()
        expect(
            self.page.get_by_role("gridcell", name=new_property["Наименование"] + "1")
        ).to_be_visible()

    @allure.step("Проверка удаления свойств объекта")
    def entity_property_remove(self, new_property):
        self.page.get_by_role("button", name="remove").click()
        expect(self.page.get_by_text("Удалить сущность?")).to_be_visible()
        self.page.get_by_role("button", name="Да").click()
        expect(
            self.page.get_by_role("gridcell", name=new_property["Наименование"] + "1")
        ).to_have_count(0)
