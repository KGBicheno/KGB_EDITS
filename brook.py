import logging
import os
import random
from datetime import date
from time import sleep
import importlib.util
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.news import News
from cogs.admin import Admin
from cogs.gaming import Gaming
from cogs.emergency import Emergency

#TODO Find out of requirements.txt works on Mac as well as *nix and Win64

terminal_core = importlib.util.spec_from_file_location("cogs.news", location='cogs/news.py')
terminal_assent = importlib.util.spec_from_file_location("cogs.gaming", location='cogs/gaming.py')
terminal_agency = importlib.util.spec_from_file_location("cogs.admin", location='cogs/admin.py')
terminal_entropy = importlib.util.spec_from_file_location("cogs.emergency", location="cogs/emergency.py")
terminal_exodus = importlib.util.spec_from_file_location("cogs.export", location="cogs/export.py")


def get_prefix(client, message):
	prefixes = ['$', '>', 'b.']

	if not message.guild:
		prefixes = ['b.']
	return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(
	command_prefix=get_prefix,
	description='EDITS: Emergency Dispatcher In Traumatic Scenarios | by KGB',
	owner_id=107221097174319104,
	case_insensitive=True
)

now = date.today()
today = now.isoformat()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_CHANNEL = os.getenv('DISCORD_NEWS_CHANNEL')
client = discord.Client()

extensions_loaded = 0

#TODO research the $is_me check you've regained your confidence in it and make it 'me' agnostic
def is_me():
	def predicate(ctx):
		return ctx.message.author.id == 107221097174319104
	return commands.check(predicate)

#TODO The on_ready() event needs some serious researching and updating
@bot.event
async def on_ready():
	liquid_guild = discord.utils.get(bot.guilds, id=107221703955841024)
	game = discord.Game("b.help for commands | b.extend for all features.")
	await bot.change_presence(activity=game)
	print(f'{bot.user} is connected to {liquid_guild.name}.\n'
	      f'{liquid_guild.name}(id {liquid_guild.id})'
	      )
	return

@bot.listen()
async def on_message(message):
	if message.author.id == bot.user.id:
		target = message.content
		if target[:4] == "KGB_E":
			await message.add_reaction('\U0001f44d') #Thumbs up
			await message.add_reaction('\U0001F44E') #Thumbs down
			await message.add_reaction('\U0000FE0F') #Alarmed/warning
			await message.add_reaction('\U0000FE0F') #Love heart
			await message.add_reaction('\U0001F494') #Broken heart
			await message.add_reaction('\U0001F9FB') #Shitrag/toilet paper
			await message.add_reaction('\U00002754') #Question/help


#TODO Have the $extend being loaded here come from brook.conf
#TODO role protect $extend and DM those roles on load to remind them to do it
#TODO check for already-loaded extensions in case of a failed load forcing multiple calls to this command
@bot.command(name="extend")
async def extend(ctx):
	"""Enables all modules"""
	#bot.load_extension('cogs.gaming')
	bot.load_extension('cogs.news')
	#bot.load_extension('cogs.admin')
	bot.load_extension('cogs.emergency')
	bot.load_extension('cogs.export')
	#bot.load_extension('cogs.board')
	News.__set_spool_state__()
	News.__set_spool_time__()
	await ctx.send("Completed")
	print("modules loaded")


#TODO Fine to keep the $sync_ratio command public but make the numbers more meaningful
@bot.command(name="sync_ratio")
async def form_the_head(ctx):
	await News.news_cog_status(terminal_core, ctx)
	sleep(2)
	await Admin.admin_cog_status(terminal_agency, ctx)
	sleep(2)
	await Gaming.gaming_cog_status(terminal_assent, ctx)
	sleep(2)
	await Emergency.emergency_cog_status(terminal_entropy, ctx)
	print("sync_ratio called: success")

#TODO Make sure the reload_morale variables come from brook.conf
@bot.command(name="reload_morale")
@commands.has_guild_permissions(administrator=True)
async def reload_gaming(ctx):
	"""Reloads the gaming module after changes or bug-fixes have been made"""
	bot.reload_extension('cogs.gaming')
	await ctx.send('Gaming module has been reloaded.')
	print("####################--GAMING RELOADED--################################")


#TODO Make sure the reload_news variables come from brook.conf
@bot.command(name="reload_news")
@commands.has_guild_permissions(administrator=True)
async def reload_news(ctx):
	"""Reloads the gaming module after changes or bug-fixes have been made"""
	bot.reload_extension('cogs.news')
	await ctx.send("News module has been reloaded")
	print("####################--NEWS RELOADED--################################")

#TODO Make sure the reload_admin variables come from brook.conf
@bot.command(name="reload_admin")
@commands.has_guild_permissions(administrator=True)
async def reload_news(ctx):
	"""Reloads the gaming module after changes or bug-fixes have been made"""
	bot.reload_extension('cogs.admin')
	await ctx.send("Admin module has been reloaded.")
	print("####################--ADMIN RELOADED--################################")

#TODO Make sure the reload_emergency variables come from brook.conf
@bot.command(name="reload_emergency")
@commands.has_guild_permissions(administrator=True)
async def reload_emergency(ctx):
	"""Reloads the emergency module after changes or bug-fixes have been made"""
	bot.reload_extension('cogs.emergency')
	await ctx.send("Emergency module has been reloaded.")
	print("####################--EMERGENCY RELOADED--################################")

#TODO the $party_cleanup command needs testing and buffing
@bot.command(name="party_cleanup")
async def clean_after_time(ctx):
	"""A blind function that clears a channel of all messages from a specific time or message id."""
	await ctx.channel.purge(after="2020-04-30 05:01:00.000+00:00")
	print("messages deleted")

# Keeping this one on the books for sentiment's sake. Hello home-ownership.
#@bot.command(name="MoveOn")
#async def move_apartment(ctx):
#	await ctx.send("Terminating epistemological fields, unbinding existing contacts. Mind seal broken.")

@bot.command(name="SitRep", hidden=True)
@commands.is_owner()
async def guild_spread(ctx):
	await ctx.author.create_dm()
	await ctx.author.send("I've compiled a list of servers on which I currently have ops. I'm ready to expand the list when you are.")
	coverage = bot.guilds
	for server in coverage:
		await ctx.author.create_dm()
		await ctx.author.send(server)

@bot.command(name="RestNow")
@commands.has_guild_permissions(administrator=True)
async def sleep_now(ctx):
	"""If an administrator needs me to log out of the server, they can invoke this script. I can then be invited back later."""
	print("Unloading Discord presence, returning to Golem.   ", ctx.author)
	await bot.close()

#TODO find what the Discord log is saying that's important and have it piped back
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger.addHandler(handler)

bot.run(TOKEN)
