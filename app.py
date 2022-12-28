'''
# Web Scraper



'''

class Config():

    def __init__(self):
        # Set all configuration variables here

        # Log of web scraper status
        self.run_log_file_path = ''
        self.run_log_webhook_url = ''

        # Log of retrieved value
        self.data_log_file_path = ''
        self.data_log_webhook_url = ''

        # Discord bot
        self.bot_token = ''

###################################
# Run app on 
###################################
if __name__ == '__main__':







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

############################
# Web Scraper
############################
if __name__ == "__main__":



    log.log('info', 'Initializing app')

    p1 = multiprocessing.Process(name='p1', target=main)
    p2 = multiprocessing.Process(name='p2', target=activate)
    p2.start()

    # Repeat this process every day -- migrate to PaaS scheduler
    while True:
        p1.start()

        log.log('info', 'Sleeping...')  
        time.sleep(60*60)
