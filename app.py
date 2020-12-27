'''
    ### Simple-Heroku-App
    This simple heroku app will serve the functionality of
    scraping the title of nike's website, saving it in a json file,
    and sending it to a discord server via webhook. The scraping
    process will include scraping the page source with selenium,
    using beautiful soup to parse the html; extracting the title.  
'''

# -- Imports

import os
import time
import json
import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import headless, scrape_website

# ----

def get_driver():
    ''' Returns a webdriver. Headless as specified in config variable. '''

    chrome_options = Options()

    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    if headless:

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        
    else:

        chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))

    return driver


def get_source(driver):
    ''' Returns the page source. Website as specified in config variable. '''

    driver.implicitly_wait(5)

    web_element = driver.get(scrape_website)

    driver.quit()

    return web_element.page_source


def parse():
    ''' Utilizes bs4 to parse page source. Returns source's title. '''




def main():
    
    driver = get_driver()

    page_source = get_source(driver)

    title = parse(page_source)


# ----

if __name__ == "__main__":
    # Repeat this process every day
    while True:
        main()
        time.sleep(86400)
