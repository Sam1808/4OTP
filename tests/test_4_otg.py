import requests
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
    mos_page.open()

    mos_page.check_header_by_text('Официальный сайт Мэра Москвы')

    mos_page.check_footer_by_text('Правительства Москвы')



    all_links = mos_page.find_elements_by_xpath("//a[@href]")

    unreachable_links = []
    main_page_links = []

    for link in all_links[:2]:
        url = link.get_attribute("href")
        main_page_links.append(url)
        response = get_response(url)
        if not response or response.status_code != 200:
            unreachable_links.append(url)

    print(unreachable_links)

    wrong_urls = []
    for link in main_page_links:
        browser.get(link)
        current_url = browser.current_url
        if link != current_url:
            wrong_urls.append(link)

    print(wrong_urls)
