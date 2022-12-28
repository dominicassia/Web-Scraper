import time, datetime, requests, json, multiprocessing, discord, discord.ext

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from app import Config 


###################################
# Primary: Web Scraper class
###################################
class WebScraper():

    def __init__(self):

        

        # Initialize bot
        self.bot = 

        # Get driver
        self.driver = self.__get_driver()
        


    def __get_driver(self):
        self.log.log('info', 'Getting driver')

        # Chrome webdriver options
        chrome_options = Options()
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.binary_location = chrome_bin

        # Prooduction
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Debug
        else:
            chrome_options.add_argument('start-maximized')

        # Create webdriver
        service = Service(executable_path=chrome_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        log.log('info', 'Done')
        return driver


    def scrape(self, url):
        self.log.log('info', f': {url}')

        self.driver.implicitly_wait(5)
        self.driver.get(url) 
        self.driver.implicitly_wait(5)

        log.log('info', f'Actual: {driver.current_url}')
        log.log('info', 'Fetching title')

        title = driver.title

        log.log('info', f'Title: {title}')
        
        driver.implicitly_wait(5)
        driver.quit()

        log.log('info', 'Done')
        return title



###################################
# Component: Logger class
###################################
class Logger():

    def __init__(self, log_fp, log_webhook):

        self.log_fp = log_file_path
        self.webhook_url = log_webhook_url

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


###################################
# Component: (Discord) Bot
###################################
class Bot(Logger):
    
    def __init__(self):
        self.client = discord.ext.commands.Bot(command_prefix='>')

    def activate(self):
        self.client.run(Config.bot_token)


@client.event
async def on_ready():
    print('[INFO] Bot is ready.')

@Bot.client.command()
async def view(ctx, *, file_path):
    logger.log('bot', f'View {file_path}')

    try:
        await ctx.send(file=discord.File(file_path))
        log.log('info', 'Done.')

    except Exception as e:
        log.log('error', 'Exception raised:')
        log.log('error', e)
        pass


@Bot.client.command()
async def scrape(ctx, *, website):
    log.log('bot', f'Scrape {website}')
    main(website)
