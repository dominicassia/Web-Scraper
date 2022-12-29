###################################
# Imports
###################################
from models import WebScraper
from os import environ as env

###################################
# Set all configuration variables here
###################################
class Config():

    def __init__(self):

        # Log of web scraper status
        self.run_log_file_path = ''
        self.run_log_webhook_url = ''

        # Log of retrieved value
        self.data_log_file_path = ''
        self.data_log_webhook_url = ''

        # Discord bot
        self.bot_token = ''

        # Chrome driver
        self.chrome_binary_path = ''
        #self.chrome_binary_path = env.get('GOOGLE_CHROME_BIN')
        self.chrome_path = ''
        #self.chrome_path = env.get('CHROMEDRIVER_PATH')

        self.headless = True


###################################
# Run app on file call
###################################
if __name__ == '__main__':

    ws = WebScraper()