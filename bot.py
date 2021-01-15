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
    print('Bot is ready.')


@client.command()
async def view(ctx, *, file_path):
    try:
        await ctx.send(file=discord.File(file_path))
    except Exception:
        pass


def activate():
    client.run(os.environ.get('bot_token'))