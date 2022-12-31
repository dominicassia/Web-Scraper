###################################
# Imports
###################################
import time, datetime, requests, json, multiprocessing, discord, discord.ext
from os import environ as env
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

###################################
# Set all configuration variables here
###################################
class Config():

    def __init__(self, debug=False):

        if debug:

            # Log of web scraper status
            self.run_log_file_path = './logs/run_log.txt'
            self.run_log_webhook_url = ''

            # Log of retrieved value
            self.data_log_file_path = './logs/data_log.json'
            self.data_log_webhook_url = ''

            # Discord bot
            self.bot_token = ''

            # Chrome driver
            self.chrome_binary_path = '/bin/google-chrome'
            self.chrome_path = './chromedriver_linux64/chromedriver'
            self.headless = True

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
# Global Component: Config class
###################################
config = Config(debug=True)

###################################
# Component: Logger class
###################################
class Logger():

    def __init__(self):

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

###################################
# Global Components: Logger class
###################################
logger = Logger()

###################################
# Primary: Web Scraper class
###################################
class WebScraper():

    def __init__(self):

        logger.log('info', 'Initializing web scraper app')

        # Get driver
        self.driver = self.__get_driver()


    def __get_driver(self):
        logger.log('info', 'Getting driver')

        # Chrome webdriver options
        chrome_options = Options()
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.binary_location = config.chrome_binary_path

        # Prooduction
        if config.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Debug
        else:
            chrome_options.add_argument('start-maximized')

        # Create webdriver
        service = Service(executable_path=config.chrome_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logger.log('info', 'Done')
        return driver


    def save_json(self, payload):
        logger.log('info', 'Saving JSON')

        try:
            # Open existing file in append mode
            with open(config.json_file_path, 'r+') as fr:

                data = dict(json.load(fr))
                data[ str(datetime.now()) ] = str(payload)

                logger.log('info', 'Data written')

        # Log file DNE 
        except FileNotFoundError:

            # Create new log file
            with open(config.json_file_path, 'r+') as fw:

                dictionary = {}
                dictionary[ str(datetime.now()) ] = payload
                json.dump(dictionary, fw)

                logger.log('info', 'New JSON file created')
        logger.log('info', 'Done')


    def send_webhook(self, payload):
        logger.log('info', 'Sending webhook')

        # Create JSON structure
        data = {
            'username'  : 'Web Scraper',
            'content'   : f'[ {str(datetime.now())} ] - {payload}'
        }

        # POST
        requests.post(
            config.data_webhook_url, 
            data        = json.dumps(data), 
            headers     = {'Content-Type': 'application/json'}
        )

        logger.log('info', 'Done')


    def __scrape_utility(self, url):
        logger.log('info', f': {url}')

        self.driver.implicitly_wait(5)
        self.driver.get(url) 
        self.driver.implicitly_wait(5)

        logger.log('info', f'Actual: {self.driver.current_url}')
        logger.log('info', 'Fetching title')

        title = self.driver.title

        logger.log('info', f'Title: {title}')
        
        self.driver.implicitly_wait(5)
        self.driver.quit()

        logger.log('info', 'Done')

        self.send_webhook(title)
        self.save_json(title)


    def scrape(self, url):
        # Create process
        self.ws_process =  multiprocessing.Process(name='ws_process', target=self.__scrape_utility, args=(url,))

        while True:
            self.ws_process.start()
            
            if config.repeat:
                logger.log('info', 'Sleeping...')  
                time.sleep(self.repeat)
            else:
                break

###################################
# Global Component: Web Scraper class
###################################
ws = WebScraper()

###################################
# Component: (Discord) Bot
###################################

client = discord.ext.commands.Bot(command_prefix='>')

def activate_bot(self):
    self.client.run(config.bot_token)

@client.event
async def on_ready():
    print('[INFO] Bot is ready.')

@client.command()
async def view(ctx, *, file_path):
    logger.log('bot', f'View {file_path}')

    try:
        await ctx.send(file=discord.File(file_path))
        logger.log('info', 'Done.')

    except Exception as e:
        logger.log('error', 'Exception raised:')
        logger.log('error', e)
        pass

@client.command()
async def scrape(ctx, *, website):
    logger.log('bot', f'Scrape {website}')
    ws.scrape(website)

###################################
# Run app on file call
###################################
if __name__ == '__main__':

    bot_process = multiprocessing.Process(name='bot_process', target=activate_bot)

    # Start bot process
    bot_process.start()

    ws.scrape('https://doma.media')