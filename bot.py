# pip3 install -U discord.py[voice]
import discord
from discord.ext import commands
import os
from decouple import config


def load_intents():
    intents = discord.Intents.default()
    intents.members = True

    return intents


def start_client(intents):
    client = commands.Bot(command_prefix='+',
                          case_insensitive=True, intents=load_intents())
    client.remove_command('help')

    return client


def load_cogs(client):
    client.load_extension('manager')

    for filename in os.listdir('commands'):
        if filename.endswith('.py'):
            client.load_extension(f'commands.{filename[:-3]}')


client = start_client(load_intents())
load_cogs(client)
TOKEN = config('TOKEN')
client.run(TOKEN)
