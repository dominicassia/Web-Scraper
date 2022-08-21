''' 
    ### Discord Bot 
    This file implements sending a saved json file
    to a discord server via a bot
'''

# -- Imports

import discord
from discord.ext import commands

from config import bot_token, log
from app import main

# ----

client = commands.Bot(command_prefix='>')


@client.event
async def on_ready():
    print('[INFO] Bot is ready.')


@client.command()
async def view(ctx, *, file_path):
    log.log('bot', f'View {file_path}')

    try:
        await ctx.send(file=discord.File(file_path))
        log.log('info', 'Done.')

    except Exception as e:
        log.log('error', 'Exception raised:')
        log.log('error', e)
        pass


@client.command()
async def scrape(ctx, *, website):
    log.log('bot', f'Scrape {website}')
    main(website)

def activate():
    client.run(bot_token)