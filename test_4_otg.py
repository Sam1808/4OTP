import requests

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def get_response(url: str):
    try:
        response = requests.get(url, timeout=10)
        return response
    except Exception:
        return None


def test_4_otg(browser):

    browser.get(url='https://www.mos.ru/')

    assert browser.find_element(By.XPATH, "//header//*[normalize-space(.)='Официальный сайт Мэра Москвы']")
    assert browser.find_element(By.XPATH, "//footer//*[contains(normalize-space(.), 'Правительства Москвы')]")

    all_links = browser.find_elements(By.XPATH, "//a[@href]")

    unreachable_links = []

    for link in all_links[:10]:
        url = link.get_attribute("href")
        response = get_response(url)
        if not response or response.status_code != 200:
            unreachable_links.append(url)

    print(unreachable_links)

    pass