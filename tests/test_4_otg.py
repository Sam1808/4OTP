import allure
import requests

from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from funcy import retry

from tests.mos_page import MosPage


@retry(tries=3, timeout=1)
def get_response(url: str):
    try:
        response = requests.get(url, timeout=10)
        return response
    except Exception:
        return None


def test_4_otg(browser):
    load_dotenv()

    mos_page = MosPage(browser)

    with allure.step('Step #1: Open https://www.mos.ru/'):
        try:
            mos_page.open()
            allure.attach(
                browser.get_screenshot_as_png(),
                name='screen',
                attachment_type=AttachmentType.PNG
            )
        except Exception:
            allure.attach(
                browser.get_screenshot_as_png(),
                name='error',
                attachment_type=AttachmentType.PNG
            )

    with allure.step('Step #2: Check Header & Footer'):
        try:
            mos_page.check_header_by_text('Официальный сайт Мэра Москвы')
            mos_page.check_footer_by_text('Правительства Москвы')
            allure.attach(
                browser.get_screenshot_as_png(),
                name='screen',
                attachment_type=AttachmentType.PNG
            )
        except Exception:
            allure.attach(
                browser.get_screenshot_as_png(),
                name='error',
                attachment_type=AttachmentType.PNG
            )

    with allure.step('Step #3: Get response from all links'):
        try:
            all_links = mos_page.find_elements_by_xpath("//a[@href]")
            unreachable_links = []
            main_page_links = []

            for link in all_links:
                url = link.get_attribute("href")
                main_page_links.append(url)
                response = get_response(url)
                if not response or response.status_code != 200:
                    unreachable_links.append(url)

            allure.attach(
                str(unreachable_links),
                name='unreachable_links',
                attachment_type=AttachmentType.TEXT
            )
        except Exception as error:
            allure.attach(
                str(error),
                name='error',
                attachment_type=AttachmentType.TEXT
            )

    with allure.step('Step #4: Check URLs'):
        try:
            wrong_urls = []
            for link in main_page_links:
                browser.get(link)
                current_url = browser.current_url
                if link != current_url:
                    wrong_urls.append(link)
            allure.attach(
                str(wrong_urls),
                name='wrong_urls',
                attachment_type=AttachmentType.TEXT
            )
        except Exception:
            allure.attach(
                browser.get_screenshot_as_png(),
                name='error',
                attachment_type=AttachmentType.PNG
            )

    errors_exist = wrong_urls or unreachable_links
    assert not errors_exist, 'Errors founds. Please check allure report'
