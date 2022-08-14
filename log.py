import datetime

class Log():
    ''' Writes to log file, prints to screen, and optionally sends webhook. '''

    def __init__(log_fp, log_webhook):
        
        # Attempt to open log file
        try:
            with open(log_fp, 'r') as f:
                pass

        # Create the log file
        except FileNotFoundError:
            with open(log_fp, 'w') as f:
                log('info', 'Log file created')

    def log(type, msg):
        '''  '''

        # Get timestamp
        timestamp = datetime.datetime.now()

        # 






def log(type, text):
    ''' Logs to txt file. '''

    now = datetime.datetime.now()
    print(f'{now}: {text}')

    if log_to_file:
        with open('src/'+log_path if local_dev else log_path, 'a') as file:
            file.write(f'{now}: {text}\n')