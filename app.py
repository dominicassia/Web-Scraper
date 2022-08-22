'''
    ### Simple-Heroku-App
    This simple heroku app will serve the functionality of
    scraping the title of nike's website, saving it in a json file,
    and sending it to a discord server via webhook. The scraping
    process will include scraping the page source with selenium,
    using beautiful soup to parse the html; extracting the title.  
'''

# Project
from config import *
from bot import activate

# General
import time
import multiprocessing
import json
import requests
from datetime import datetime

# Webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# --- // --- #

def get_driver():
    ''' Returns a webdriver. Headless and chrome bin as specified in config var'''

    log.log('info', 'Getting driver')

    # Chrome webdriver options
    chrome_options = Options()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = chrome_bin

    # Prooduction
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

    # Debug
    else:
        chrome_options.add_argument('start-maximized')

    # Create webdriver
    service = Service(executable_path=chrome_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    log.log('info', 'Done')
    return driver


def get_title(driver, scrape_website):
    ''' Get title given Chrome driver '''

    log.log('info', f'Fetching: {scrape_website}')

    driver.implicitly_wait(5)
    driver.get(scrape_website) 
    driver.implicitly_wait(5)

    log.log('info', f'Actual: {driver.current_url}')
    log.log('info', 'Fetching title')

    title = driver.title

    log.log('info', f'Title: {title}')
    
    driver.implicitly_wait(5)
    driver.quit()

    log.log('info', 'Done')
    return title


def save_json(title):
    ''' Saves the title to a json file. Returns nothing. '''

    log.log('info', 'Saving JSON')

    try:
        # Open existing file in append mode
        with open(json_file_path, 'r+') as fr:

            data = dict(json.load(fr))
            data[ str(datetime.now()) ] = str(title)

            log.log('info', 'Data written')

    # Log file DNE 
    except FileNotFoundError:

        # Create new log file
        with open(json_file_path, 'r+') as fw:

            dictionary = {}
            dictionary[ str(datetime.now()) ] = title
            json.dump(dictionary, fw)

            log.log('info', 'New JSON file created')
    log.log('info', 'Done')


def send_webhook(title):
    ''' Utilizes requests to send webhook. Returns nothing. '''

    log.log('info', 'Sending webhook')

    # Create JSON structure
    data = {
        'username'  : 'Web Scraper',
        'content'   : f'[ {str(datetime.now())} ] - {title}'
    }

    # POST
    requests.post(
        data_webhook_url, 
        data        = json.dumps(data), 
        headers     = {'Content-Type': 'application/json'}
    )

    log.log('info', 'Done')


def main(website=scrape_website):

    log.log('info', 'Launching web scraper')

    # Begin execution
    try:
        driver = get_driver()
        title = get_title(driver, website)
        save_json(title)
        send_webhook(title)

        log.log('info', 'Scrape complete')

    # Catch and log exception
    except Exception as e:
        log.log('error', 'Exception raised:')
        log.log('error', e)

# --- // --- #

if __name__ == "__main__":
    ''' On file call '''
    
    log.log('info', 'Initializing app')

    p1 = multiprocessing.Process(name='p1', target=main)
    p2 = multiprocessing.Process(name='p2', target=activate)
    p2.start()

    # Repeat this process every day -- migrate to PaaS scheduler
    while True:
        p1.start()

        log.log('info', 'Sleeping...')  
        time.sleep(60*60)
