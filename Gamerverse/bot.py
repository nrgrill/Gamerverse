import datetime
from discord.ext import commands, tasks
from discord import Guild
import discord
from dataclasses import dataclass
from gamerverse.models import Event, User

BOT_TOKEN = "MTE3MDU0NDMzMjg5MDE4NTgyOA.GyvMAE.I-1U1rYXW-KDkUQ4MeM9Vc4TsEtaRmNFU_aPAo"
CHANNEL_ID = 1170556401265934376

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
channel = bot.get_channel(CHANNEL_ID)

@bot.event
async def on_ready():
    print("Hello! Gamerverse bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Gamerverse bot is ready!")
    
@bot.command()
async def test_func(ctx, eventID):
    guild = ctx.message.guild
    event = Event.query.get(id=eventID)
    await guild.create_scheduled_event(name=event.title,
                start_time=event.start_date,
                end_time=event.end_date,
                entity_type=discord.EntityType.external,
                location=event.location,
                privacy_level=discord.PrivacyLevel.guild_only)    
    
bot.run(BOT_TOKEN)