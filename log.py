import datetime, requests, json

class Log():
    ''' Writes to log file, prints to screen, and optionally sends webhook. '''

    def __init__(self, log_fp, log_webhook):

        self.log_fp = log_fp
        self.webhook_url = log_webhook

        # Attempt to open log file
        try:
            with open(log_fp, 'r') as f:
                pass

        # Create the log file
        except FileNotFoundError:
            with open(log_fp, 'w') as f:
                self.log('info', 'Log file created')

    def log(self, type, msg):
        ''' Write, print, send log message '''

        # Get timestamp
        timestamp = datetime.datetime.now()

        # Create string
        log_msg = f'[{type.upper()}, {timestamp}] - {msg}\n'

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