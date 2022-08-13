''' 
    ### Discord Bot 
    This file implements sending a saved json file
    to a discord server via a bot
'''

# -- Imports

import os
import discord
from discord.ext import commands

# ----

client = commands.Bot(command_prefix='>')


@client.event
async def on_ready():
    print('[INFO] Bot is ready.')


@client.command()
async def view(ctx, *, file_path):
    print(f'[INFO] View: {file_path}\n')
    try:
        await ctx.send(file=discord.File(file_path))
        print('[SUCCESS]\n')
    except Exception:
        print('[Error]\n')
        pass


def activate():
    client.run(os.environ.get('bot_token'))