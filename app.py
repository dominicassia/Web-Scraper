###################################
# Imports
###################################
from models import WebScraper
from os import environ as env

###################################
# Set all configuration variables here
###################################
class Config():

    def __init__(self, debug=False):
x
        if debug:

            # Log of web scraper status
            self.run_log_file_path = './run_log.txt'
            self.run_log_webhook_url = ''

            # Log of retrieved value
            self.data_log_file_path = './data_log.json'
            self.data_log_webhook_url = ''

            # Discord bot
            self.bot_token = ''

            # Chrome driver
            self.chrome_binary_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
            self.chrome_path = './chromedriver/chromedriver.exe'
            self.headless = False

            # Web scraper scheduling
            self.repeat = None

        else:

            # Log of web scraper status
            self.run_log_file_path = env.get('run_log_file_path')
            self.run_log_webhook_url = env.get('run_log_webhook_url')

            # Log of retrieved value
            self.data_log_file_path = env.get('data_log_file_path')
            self.data_log_webhook_url = env.get('data_log_webhook_url')

            # Discord bot
            self.bot_token = env.get('bot_token')

            # Chrome driver
            self.chrome_binary_path = env.get('chrome_binary_path')
            self.chrome_path = env.get('chrome_path')
            self.headless = True

            # Web scraper scheduling
            self.repeat = env.get('repeat')


###################################
# Run app on file call
###################################
if __name__ == '__main__':

    ws = WebScraper()
    ws.scrape('https://doma.media')