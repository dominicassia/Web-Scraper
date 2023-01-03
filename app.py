###################################
# Imports
###################################
from config import Config
from logger import Logger
from scraper import WebScraper
from discord.ext import commands
import  multiprocessing
import discord

###################################
# Primary Component: Discord Bot
###################################
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

###################################
# Application core
###################################\
class App():

    def __init__(self):
        # Create config object
        self.config = Config(debug=True)

        # Create logger object
        self.logger = Logger()

        # Create bot process
        bot_process = multiprocessing.Process(name='bot_process', target=client.run(self.config.bot_token))

        # Create web scraper object
        self.ws = WebScraper(self.config, self.logger)

        # Start bot process
        bot_process.start()

# Instantiate
app = App()

###################################
# Primary Component: Discord Bot Commands
###################################
@client.event
async def on_ready():
    print('[INFO] Bot is ready.')

@client.command()
async def restart():
    app.logger.log('bot', f'Restarting')
    #main()

@client.command()
async def view(ctx, *, file_path):
    app.logger.log('bot', f'View {file_path}')

    try:
        await ctx.send(file=discord.File(file_path))
        app.logger.log('info', 'Done.')

    except Exception as e:
        app.logger.log('error', 'Exception raised:')
        app.logger.log('error', e)
        pass

@client.command()
async def scrape(ctx, *, website):
    app.logger.log('bot', f'Scrape {website}')
    app.ws.scrape(website)