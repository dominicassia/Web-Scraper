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


@client.event
async def on_member_join(member):
    print(f'Welcome to the server {member}!')


@client.command()
async def view(ctx, *, file_path):
    await ctx.send(file=discord.File(file_path))


client.run(os.environ.get('bot_token'))