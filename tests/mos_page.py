import os
import time
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException


class MosPage:
    def __init__(self, browser):
        self.browser = browser
        self.url = 'https://www.mos.ru/'
        self.timeout = int(os.getenv('TIMEOUT') or 30)

    def open(self):
        self.browser.get(self.url)

    def find_element_by_xpath(self, xpath):
        for attempt in range(self.timeout):
            try:
                element = self.browser.find_element(By.XPATH, xpath)
                return element
            except NoSuchElementException:
                if attempt + 1 == self.timeout:
                    raise NoSuchElementException(
                        f'Element {xpath} not found during {self.timeout} seconds'
                    )
                time.sleep(1)

    def find_elements_by_xpath(self, xpath):
        for attempt in range(self.timeout):
            try:
                elements_collection = self.browser.find_elements(By.XPATH, xpath)
                return elements_collection
            except NoSuchElementException:
                if attempt + 1 == self.timeout:
                    raise NoSuchElementException(
                        f'Elements collection {xpath} not found during {self.timeout} seconds'
                    )
                time.sleep(1)

    def check_header_by_text(self, text):
        xpath = f"//header//*[contains(normalize-space(.), '{text}')]"
        header = self.find_element_by_xpath(xpath)
        return header

    def check_footer_by_text(self, text):
        xpath = f"//footer//*[contains(normalize-space(.), '{text}')]"
        footer = self.find_element_by_xpath(xpath)
        return footer
