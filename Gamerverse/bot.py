import datetime
from discord.ext import commands, tasks
from discord import Guild
import discord
from dataclasses import dataclass
from gamerverse.models import Event,User
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from gamerverse import * 
import gamerverse.posts.routes as p

#from gamerverse import db, mail
# import 

from flask import Flask
import pytest


# posts = Blueprint('bot', __name__)

BOT_TOKEN = "MTE3MDU0NDMzMjg5MDE4NTgyOA.Gz_W8u.6PnO5AxNW8evnAtB38VDUJFCt3bJguW9gAKNJ8"
CHANNEL_ID = 1170556401265934376

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
channel = bot.get_channel(CHANNEL_ID)


@bot.event
async def on_ready():
    print("Hello! Gamerverse bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Gamerverse bot is ready!")

# @posts.route("/bot/<int:post_id>")
@bot.command()
async def create_discord_event(ctx):
    try:
        guild = ctx.message.guild
        print("guild ctx")
        event = p.discord_connector(4) # python sqllite library handles this
        print("discord connector")
        await guild.create_scheduled_event(name=event.title,
                start_time=event.start_date,
                end_time=event.end_date,
                entity_type=discord.EntityType.external,
                location=event.location,
                privacy_level=discord.PrivacyLevel.guild_only)   
    except Exception as e:
        print(e)
    
bot.run(BOT_TOKEN)