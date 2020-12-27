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
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import headless, scrape_website, webhook_url

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

    driver = webdriver.Chrome(options=chrome_options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))

    return driver


def get_source(driver):
    ''' Returns the page source. Website as specified in config variable. '''

    driver.implicitly_wait(5)

    driver.get(scrape_website)

    page_source = driver.page_source

    driver.quit()

    return page_source


def parse(page_source):
    ''' Utilizes bs4 to parse page source. Returns source's title. '''

    soup = BeautifulSoup(page_source, 'html.parser')

    title = soup.find('title')

    return title


def save_json(title):
    ''' Saves the title to a json file. Returns nothing. '''

    file_location = './data.json'

    try:

        with open(file_location, 'r') as fr:

            data = json.load(fr)

            data[ str(datetime.datetime.now()) ] = title

            with open(file_location, 'w') as fw:

                json.dump(data, fw)
     

    except FileNotFoundError:

        with open(file_location, 'w') as fw:

            dictionary = {}

            dictionary[ str(datetime.datetime.now()) ] = title

            json.dump(dictionary, fw)


def send_webhook(title):
    ''' Utilizes requests to send webhook. Returns nothing. '''

    data = {
        'username'  : 'simple-heroku-app',
        'content'   : f'[{datetime.datetime.now()}] - {title}'
    }

    requests.post(
        webhook_url, 
        data        = json.dumps(data), 
        headers     = {'Content-Type': 'application/json'}
    )


def main():
    
    driver = get_driver()

    page_source = get_source(driver)

    title = parse(page_source)

    # save_json(title)

    send_webhook(title)

# ----

if __name__ == "__main__":
    # Repeat this process every day
    while True:
        main()
        time.sleep(86400)
