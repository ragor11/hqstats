

import discord
import asyncio
import json
import urllib.request, json
import random
import os
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import requests
import re as regex

# Import from extensions

from discord.ext import commands
from discord.ext.commands import Bot

# Preparatory code

client = Bot(command_prefix='~')
hqSports = "https://cdn.discordapp.com/attachments/478328786681856014/481536306426413086/BHgEmJt4_400x400.png"
hq = "https://images-ext-2.discordapp.net/external/4KwUyDXQajeezUXXt7xbDf2YcdlIAROnPcx4s0VSEqQ/https/plusreed.com/assets/bear/HQ.png"
keyClient = str(os.environ.get('TOKEN',3))
headers = {'x-hq-client': 'Android/1.14.4', 'x-hq-country': 'CA', 'x-hq-lang': 'en', 'x-hq-timezone': 'America/Toronto', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjE4NDEzMjk4LCJ1c2VybmFtZSI6Ik1vbnUyMzciLCJhdmF0YXJVcmwiOiJzMzovL2h5cGVzcGFjZS1xdWl6L2EvNDUvMTg0MTMyOTgtYTNKTUptLmpwZyIsInRva2VuIjpudWxsLCJyb2xlcyI6W10sImNsaWVudCI6IiIsImd1ZXN0SWQiOm51bGwsInYiOjEsImlhdCI6MTU1MzU2NDkwMSwiZXhwIjoxNTYxMzQwOTAxLCJpc3MiOiJoeXBlcXVpei8xIn0.wAJOJtuHa5xYbtCjfQgKSWSOJND55DU4Za_mtzzwHy8', 'x-hq-stk': 'MQ==', 'Host': 'api-quiz.hype.space', 'Connection': 'Keep-Alive', 'Agent-Encoding': 'gzip', 'User-Agent': 'okhttp/3.10.0'}
url = "https://api-quiz.hype.space"
welcome = ["Hey, @everyone! It's HQ Time!"]
@client.event
async def on_ready():
	print ("Starting bot...")
	print(client.user.name)
	print(client.user.id)
	
# !purge (number)
	
@client.event
async def on_message(message):
	if message.content.startswith('~clear'):
		tmp = await client.send_message(message.channel, 'Clearing messages...')
		async for msg in client.logs_from(message.channel):
			await client.delete_message(msg)
	elif message.content.startswith('!shows'):
		with urllib.request.urlopen("https://api-quiz.hype.space/shows/now") as url:
			data = json.loads(url.read().decode())
			timeGame = data['nextShowTime']
			timeGame = dateutil.parser.parse(timeGame) + timedelta(hours=-4)
			timeGame = timeGame.strftime('%I:%M%p %A, %B %d, %Y')
			color = int("0x" + data['upcoming'][0]['nextShowLabel']['color'][1:], 0)
			embed=discord.Embed(color=color)
			if data['upcoming'][0]['nextShowLabel']['title']=="HQ Trivia":
				embed.set_thumbnail(url=hq)
			else:	
				embed.set_thumbnail(url=hqSports)
			if data['active']==False:
				embed.add_field(name= timeGame, value="Prize: " + data['nextShowPrize'], inline=True)
				embed.set_footer(text="Type: " + data['upcoming'][0]['nextShowLabel']['title'])
			else:
				embed.add_field(name=data['upcoming'][0]['nextShowLabel']['title'] + "is live!", value="Prize: " + data['nextShowPrize'])
			await client.send_message(message.channel, embed=embed)
			if data['active'] == True:
				await client.send_message(message.channel, (random.choice(welcome)))
	elif message.content.startswith('!winnings'):
		winargs = message.content.split(" ")
		winargs = winargs[1:]
		winargs = [float(i) for i in winargs]
		messagewinners = "Winnings: $",round(winargs[0]/winargs[1],2)," split across ",winargs[1]," winners!"
		await client.send_message(message.channel, "Winnings: ${} split across {} winners!".format(round(winargs[0]/winargs[1],2),int(winargs[1])))
	elif message.content.startswith('!hqstats'):
		winargs = message.content.split(" ")
		winargs = winargs[1:]
		data = requests.get("https://api-quiz.hype.space/users?q=" + winargs[0], headers=headers)
		datap = json.loads(data.text)
		id = str(datap['data'][0]['userId'])
		id = str(id)
		data = requests.get("https://api-quiz.hype.space/users/" + id, headers=headers)
		datap = json.loads(data.text)
		winnings = (datap['leaderboard']['total'][1:])
		winnings = float(regex.sub("[$,]", "", winnings))
		embed=discord.Embed(title="HQ Stats for user " + datap['username'], description="CHECK MORE - https://stats.hqtrivia.pro/")
		embed.set_thumbnail(url=datap['avatarUrl'])
		embed.add_field(name="User Id: " + str(datap['userId']), value="Wins: " + str(datap['winCount']), inline=True)
		embed.add_field(name="Games played: " + str(datap['gamesPlayed']),value="Winnings: " + datap['leaderboard']['total'], inline=True)
		if datap['winCount'] > 0:
			embed.set_footer(text=("Avg Winnings/Game: $" + str(round(winnings/int(datap['gamesPlayed']),2))))
		else:
			embed.set_footer(text=("Avg Winnings/Game: 0"))
		await client.send_message(message.channel, embed=embed)
			#client.send_message(message.channel, "Something went wrong. Try again!")
			#print("failure 69 lolel")

# bot.run
client.run("NjE5ODQ2NDYwNzU3NzcwMjQw.XXxMQQ.aQDAOYvx4WZNU0zhLgYsKdbw9j4")
