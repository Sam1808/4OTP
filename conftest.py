from pytest import fixture
from selenium.webdriver import Chrome


@fixture
def browser():
    browser = Chrome()
    browser.set_window_size(1920, 1080)
    yield browser
    browser.quit()
