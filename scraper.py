###################################
# Imports
###################################
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import multiprocessing
import requests
import json
import time

###################################
# Primary Component: Web Scraper class
###################################
class WebScraper():

    def __init__(self, config, logger):

        self.logger = logger
        self.config = config

        self.logger.log('info', 'Initializing web scraper app')

        # Get driver
        self.driver = self.__get_driver()


    def __get_driver(self):
        self.logger.log('info', 'Getting driver')

        # Chrome webdriver options
        chrome_options = Options()
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.binary_location = self.config.chrome_binary_path

        # Prooduction
        if self.config.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Debug
        else:
            chrome_options.add_argument('start-maximized')

        # Create webdriver
        driver = webdriver.Chrome(options=chrome_options)
        
        self.logger.log('info', 'Done')
        return driver


    def save_json(self, payload):
        self.logger.log('info', 'Saving JSON')

        try:
            # Open existing file in append mode
            with open(self.config.data_log_file_path, 'r+') as fr:

                data = dict(json.load(fr))
                data[ str(datetime.now()) ] = str(payload)

                self.logger.log('info', 'Data written')

        # Log file DNE 
        except FileNotFoundError:

            # Create new log file
            with open(self.config.data_log_file_path, 'w') as fw:

                dictionary = {}
                dictionary[ str(datetime.now()) ] = payload
                json.dump(dictionary, fw)

                self.logger.log('info', 'New JSON file created')
        self.logger.log('info', 'Done')


    def send_webhook(self, payload):
        self.logger.log('info', 'Sending webhook')

        # Create JSON structure
        data = {
            'username'  : 'Web Scraper',
            'content'   : f'[ {str(datetime.now())} ] - {payload}'
        }

        # POST
        requests.post(
            self.config.data_log_webhook_url, 
            data        = json.dumps(data), 
            headers     = {'Content-Type': 'application/json'}
        )

        self.logger.log('info', 'Done')


    def __scrape_utility(self, url):
        self.logger.log('info', f': {url}')

        self.driver.implicitly_wait(5)
        self.driver.get(url) 
        self.driver.implicitly_wait(5)

        self.logger.log('info', f'Actual: {self.driver.current_url}')
        self.logger.log('info', 'Fetching title')

        title = self.driver.title

        self.logger.log('info', f'Title: {title}')
        
        self.driver.implicitly_wait(5)
        self.driver.quit()

        self.logger.log('info', 'Done')

        self.send_webhook(title)
        self.save_json(title)


    def scrape(self, url):
        # Create process
        self.ws_process =  multiprocessing.Process(name='ws_process', target=self.__scrape_utility, args=(url,))

        while True:
            self.ws_process.start()
            
            if self.config.repeat:
                self.logger.log('info', 'Sleeping...')  
                time.sleep(self.repeat)
            else:
                break