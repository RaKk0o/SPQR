import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

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
    await bot.tree.sync()
    scheduler.start()
    print("Scheduler started")

@bot.tree.command(name="spqr", description="Vérifiez la signification de l'anagramme SPQR")
@app_commands.describe(s="Lettre S", p="Lettre P", q="Lettre Q", r="Lettre R")
async def spqr(interaction: discord.Interaction, s: str, p: str, q: str, r: str):
    user_id = interaction.user.id
    current_time = time.time()
    cooldown = 24 * 60 * 60  # 24 heures en secondes

    if user_id in last_used:
        elapsed_time = current_time - last_used[user_id]
        if elapsed_time < cooldown:
            remaining_time = int((cooldown - elapsed_time) / 60)  # Convertir en minutes
            await interaction.response.send_message(f"Vous devez attendre {remaining_time} minutes avant de pouvoir réutiliser cette commande.", ephemeral=True)
            return

    # Mettre à jour l'horodatage de la dernière utilisation
    last_used[user_id] = current_time

    # Les valeurs correctes
    correct_values = {
        'S': os.getenv('SPQR_S').lower(),
        'P': os.getenv('SPQR_P').lower(),
        'Q': os.getenv('SPQR_Q').lower(),
        'R': os.getenv('SPQR_R').lower()
    }

    # Vérification des valeurs fournies
    if s.lower() == correct_values['S'] and p.lower() == correct_values['P'] and q.lower() == correct_values['Q'] and r.lower() == correct_values['R']:
        results = ['Bonne réponse, tu viens de gagner 1 Million mon con !']
    else:
        results = [f'Mauvaise réponse ! Ce n\'est pas {s} {p} {q} {r}']

    # Envoi des résultats
    await interaction.response.send_message('\n'.join(results))

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

    if 'chat' in message.content.lower():
        api_key = os.getenv('CAT_API_KEY')
        response = requests.get('https://api.thecatapi.com/v1/images/search', headers={'x-api-key': api_key})
        data = response.json()
        await message.channel.send(data[0]['url'])

    if 'fee' in message.content.lower() or "fée" in message.content.lower():
        await message.channel.send('TA GUEULE!')

async def send_daily_gif():
    channel_id = int(os.getenv('CHANNEL_ID'))
    gif_url = "https://tenor.com/view/a-roulette-kaamelott-gif-25967290"
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(gif_url)

scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_gif, CronTrigger(hour=15, minute=0, second=0, timezone='Asia/Tokyo'))

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
