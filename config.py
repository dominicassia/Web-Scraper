''' Various app configuration variables. '''
from os import environ as env
from log import *

# Json & log
json_file_path  = './data.json'
log_file_path   = './log.txt'

log_webhook_url = env.get('log_webhook_url')

# Init logger
log = Log(log_file_path, log_webhook_url)

# Webdriver
headless        = True
chrome_bin      = env.get('GOOGLE_CHROME_BIN')
chrome_path     = env.get("CHROMEDRIVER_PATH")

data_webhook_url    = env.get('data_webhook_url')
scrape_website      = env.get('scrape_website')