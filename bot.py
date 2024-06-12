import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
