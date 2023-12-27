import discord
from os import environ
from src.bot import SivBot

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    client = SivBot(intents=intents)
    client.run(environ.get('SECRET_TOKEN'))
