# bot.py
import os
import hypixel_stats
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)
hypixel_statistics = hypixel_stats.HypixelStats()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='bedwars', help='Gives stats for bedwars games.')
async def bedwars_stats(ctx, mode, username):
    if mode == 'solos':
        msg = hypixel_statistics.bedwars_stats_solos(username)
    elif mode == 'duos':
        msg = hypixel_statistics.bedwars_stats_duos(username)
    elif mode == 'trios':
        msg = hypixel_statistics.bedwars_stats_trios(username)
    elif mode == 'quads':
        msg = hypixel_statistics.bedwars_stats_quads(username)
    elif mode == 'practice':
        msg = hypixel_statistics.bedwars_stats_practice(username)
    else:
        msg = "Usage: bedwars {mode} {username}\nmode options are: solos, duos, trios, quads and practice"
    await ctx.send(msg)

@bot.command(name="im_mister_money_bags")
async def money_bags(ctx):
    msg = "YO YO YO!"
    await ctx.send(msg)


bot.run(TOKEN)

