import allure

from conftest import logins_pwd


class TimeoutException:
    pass


class BasePage:
    def __init__(self, page):
        self.page = page

    @allure.step("Открытие сайта")
    def open_site(self, url):
        self.page.add_init_script("""
            HTMLInputElement.prototype.click = function() {
                this.dispatchEvent(new Event('change', { bubbles: true }));
            };
        """)
        self.page.goto(url, wait_until="networkidle")

    @allure.step("Авторизация на сайте")
    def login(self, login):
        self.page.get_by_role("textbox", name="логин").click()
        self.page.get_by_role("textbox", name="логин").fill(login)
        self.page.get_by_role("textbox", name="Пароль").click()
        self.page.get_by_role("textbox", name="Пароль").fill(logins_pwd(login))
        self.page.get_by_role("button", name="Войти").click()

    def check_element(self, locator):
        try:
            return self.page.locator(locator)
        except TimeoutException:
            return False
