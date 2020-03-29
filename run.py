import discord
import requests
import threading
from flask import Flask, render_template, request
from threading import Thread
from discord.ext import tasks
from json import load
settings = load(open("settings.json"))
app = Flask(__name__)

client = discord.Client()

@client.event
async def on_ready():
    statuscheck.start()
    print('로그인:', client.user)
    print("{} User | {} Channels | {} Guilds".format(len(client.users), len([*client.get_all_channels()]), len(client.guilds)))

@tasks.loop(seconds=2)
async def statuscheck():
    global guilds
    global users
    global channels
    global guildlists
    guilds = len(client.guilds)    
    users = len(client.users)
    channels = len([*client.get_all_channels()])
    guildlists=[f"{guild.name}" for guild in client.guilds]
    
@app.route('/')
def index():
    return render_template('index.html',
    guild=guilds,
    user=users,
    channel=channels,
    guildlist=guildlists
    )

def bot():
    client.run(settings['discordBot']['token'])
    
if __name__ == '__main__':
    task = threading.Thread(target=bot)
    task.start()
    app.run(host='0.0.0.0', port=80)
