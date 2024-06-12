import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="Voici une liste de commandes disponibles :")
        for cog, commands in mapping.items():
            for command in commands:
                embed.add_field(name=f"!{command.name}", value=command.help or "No description", inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command(name='hello', help='Dit bonjour, il est bien élevé.')
async def hello(ctx):
    await ctx.send('Salut les espéquhériens!')

@bot.command(name='chat', help="Envoie une photo aléatoire de chat.")
async def cat(ctx):
    api_key = os.getenv('CAT_API_KEY')
    response = requests.get('https://api.thecatapi.com/v1/images/search', headers={'x-api-key': api_key})
    data = response.json()
    await ctx.send(data[0]['url'])

@bot.command(name='canard', help="Envoie une photo aléatoire de canard.")
async def duck(ctx):
    response = requests.get('https://random-d.uk/api/v2/quack')
    data = response.json()
    await ctx.send(data['url'])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Vérifier si le message contient le mot "coin"
    if 'coin' in message.content.lower():
        response = requests.get('https://random-d.uk/api/v2/quack')
        data = response.json()
        await message.channel.send(data['url'])

    await bot.process_commands(message)

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
