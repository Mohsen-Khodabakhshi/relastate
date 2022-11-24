import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

import csv


class ChromeCrawler:
    def __init__(self, debug=True, executable_path: str = "./chromedriver") -> None:
        self.debug = debug
        self.selenium_driver = self.start_selenium_driver(executable_path)

    def start_selenium_driver(self, executable_path: str):
        if self.debug:
            return uc.Chrome(executable_path=executable_path)
            
        chrome_options = uc.ChromeOptions()
        chrome_options.headless=True

        return uc.Chrome(executable_path=executable_path, options=chrome_options)

    def get_by_xpath(self, xpath: str) -> list:
        return self.selenium_driver.find_elements(By.XPATH, xpath)

    def get_by_id(self, id_: str) -> list:
        return self.selenium_driver.find_elements(By.ID, id_)

    def save_to_csv(self, data: dict):
        with open('output.csv', 'a') as f:
            w = csv.DictWriter(f, data.keys())
            w.writerow(data)
