''' Various app configuration variables. '''
from os import environ as env
from log import Log

# Json & log
json_file_path  = './data.json'
log_file_path   = './log.txt'

log = Log(log_file_path)

# Webdriver
headless        = True
chrome_bin      = env.get('GOOGLE_CHROME_BIN')
chrome_path     = env.get("CHROMEDRIVER_PATH")

webhook_url     = env.get('webhook_url')
scrape_website  = env.get('scrape_website')