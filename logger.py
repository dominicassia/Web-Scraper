###################################
# Imports
###################################
from datetime import datetime
import requests
import json

###################################
# Secondary Component: Logger class
###################################
class Logger():

    def __init__(self, config):

        self.log_fp = config.run_log_file_path
        self.webhook_url = config.run_log_webhook_url

        # Attempt to open log file
        try:
            with open(self.log_fp, 'r') as f:
                pass

        # Create the log file
        except FileNotFoundError:
            with open(self.log_fp, 'w') as f:
                self.log('info', 'Log file created')

    def log(self, type, msg):

        # Get timestamp
        timestamp = datetime.now()

        # Create string
        log_msg = f'[{type.upper()}, {timestamp}] - {msg}'

        # Write to log
        with open(self.log_fp, 'r+') as f:
            f.write(log_msg)

        # Print to screen
        print(log_msg)

        # Send webhook
        data = {
            'username'  : 'Logger',
            'content'   : log_msg
        }

        requests.post(
            self.webhook_url, 
            data        = json.dumps(data), 
            headers     = {'Content-Type': 'application/json'}
        )