###################################
# Imports
###################################
from os import environ as env
from tokens import bot_token, run_log_webhook_url, data_log_webhook_url

###################################
# Set all configuration variables here
###################################
class Config():
    def __init__(self, debug=False):
        if debug:
            # Log of web scraper status
            self.run_log_file_path = './logs/run_log.txt'
            self.run_log_webhook_url = run_log_webhook_url

            # Log of retrieved value
            self.data_log_file_path = './logs/data_log.json'
            self.data_log_webhook_url = data_log_webhook_url

            # Discord bot
            self.bot_token = bot_token

            # Chrome driver
            self.chrome_binary_path = '/usr/bin/google-chrome-stable'
            self.headless = True

            # Web scraper scheduling
            self.repeat = 30
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
            self.headless = True

            # Web scraper scheduling
            self.repeat = env.get('repeat')