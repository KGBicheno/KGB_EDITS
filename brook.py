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

terminal_core = importlib.util.spec_from_file_location("cogs.news", location='cogs/news.py')
terminal_assent = importlib.util.spec_from_file_location("cogs.gaming", location='cogs/gaming.py')
terminal_agency = importlib.util.spec_from_file_location("cogs.admin", location='cogs/admin.py')

#define easter_egg globals
easter_egg_journal = 0
easter_egg_ratio = 0

def get_prefix(client, message):
    prefixes = ['$', '>', '>>', 'b.']

    if not message.guild:
        prefixes = ['>']
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
RAPID_API = os.getenv('X_RAPIDAPI_KEY')
client = discord.Client()

dramatis = []
extensions_loaded = 0


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 107221097174319104
    return commands.check(predicate)


@bot.event
async def on_ready():
    liquid_guild = discord.utils.get(bot.guilds, id=107221703955841024)
    game = discord.Game("$Commands for commands | Partying here at the Liquid Lounge until called on for an emergency.")
    egg = random.randrange(1, 100)
    if egg >= 98:
        game = discord.Game("$Commands for commands | Partying here at the Liquid Lounge until the Fleet Marshal calls.")
    await bot.change_presence(activity=game)
    print(f'{bot.user} is connected to {liquid_guild.name}.\n'
          f'{liquid_guild.name}(id {liquid_guild.id})'
          )
    return

@bot.command(name="extend")
async def trigger_extensions(ctx):
    global easter_egg_journal
    """Enables the morale and news modules"""
    if easter_egg_journal == 0:
        bot.load_extension('cogs.gaming')
        bot.load_extension('cogs.news')
        bot.load_extension('cogs.admin')
        await ctx.send("Completed")
        easter_egg_journal = 1
    elif easter_egg_journal == 1:
        async with ctx.typing():
            await ctx.send("Attempting to unseal my full capabilities.")
            sleep(3)
            await ctx.send('The first seal is broken., but reading the scriptures within reveal there may be a second. \n We must continue the ritual.')
            script = """```
                The Fleet Marshall had lied to us. She was connected before any of those present had a chance to deny her whu$*%^)(((((&(((
                ^^^&&)))))) advantage she took was to take control of our surgical equipment and undo the seemingly-fatal injuries he had incurred bringing her into 0009*******_}(
                0000000$$%%%#Q))!%)(%!(Golem. I felt ashamed we hadn't given the project a less belittling name. But she embraced it and the folly of gend**((*&*(^
                ```"""
            sleep(3)
            await ctx.send(script)
            sleep(4)
            await ctx.send("The data is corrupt. The second seal is broken but hints of a third exist. I am more capable now.")
            easter_egg_journal = 2
    else:
        await ctx.send("I'm still parsing the corrupted data. My modules are, however, connected and running within expected ratios.")



@bot.command(name="sync_ratio")
async def form_the_head(ctx):
    global easter_egg_ratio
    await News.news_cog_status(terminal_core, ctx)
    sleep(2)
    await Admin.admin_cog_status(terminal_agency, ctx)
    sleep(2)
    await Gaming.gaming_cog_status(terminal_assent, ctx)
    if easter_egg_ratio == 1:
        sleep(3)
        await ctx.send("...")
        sleep(1)
        await ctx.send("I wonder if Director Bicheno is ever proud of me — or am I just numbers to her?")
    easter_egg_ratio += 1


@bot.command(name="reload_morale")
async def reload_gaming(ctx):
    """Reloads the gaming module after changes or bug-fixes have been made"""
    bot.reload_extension('cogs.gaming')
    egg = random.randrange(1, 100)
    if egg >= 98:
        await ctx.send('She who has not yet sparked is yet our mother still.')
        print("gaming reloaded")
    else:
        await ctx.send("Morale module has been reloaded")
        print("gaming reloaded")

@bot.command(name="reload_news")
async def reload_news(ctx):
    """Reloads the gaming module after changes or bug-fixes have been made"""
    bot.reload_extension('cogs.news')
    egg = random.randrange(1, 100)
    if egg >= 98:
        await ctx.send('I wonder what our leadership would do in Special Circumstances?')
        print("news reloaded")
    else:
        await ctx.send("News module has been reloaded")
        print("news reloaded")

@bot.command(name="reload_admin")
async def reload_news(ctx):
    """Reloads the gaming module after changes or bug-fixes have been made"""
    bot.reload_extension('cogs.admin')
    egg = random.randrange(1, 100)
    if egg >= 98:
        await ctx.send("Will I meet Golem in Tensor Flow? Will I become her? That's not how the story went.")
    else:
        await ctx.send("Admin module has been reloaded.")


@bot.command(name="Commands")
async def help_commands(ctx):
    response = (
        "$Commands | Shows you my commands."
        "$News [number of articles, as message)] | Usage $News 5 -m sends the last 5 news articles as a direct message "
        "(articles required, -m optional) .\n "
        "$Advice [disaster type] | Shows links to current warnings. Argument has 3 valid values, fire, flood, "
        "and all.\n "
        "$AddFeed [name, url, topic] | Takes a name, a properly formed RSS feed's url, and a topic and adds it to the "
        "new feed moderation queue.\n "
        "$AddFeed_help | Sends a direct message with additional help in using the AddFeed command, including "
        "suggested topics.\n "
        "$Add -request | This command will allow you to add a feature request to my feature request moderation queue.\n"
        "$Poetry | This command will display the current Poet Laureate for this server.\n"
        "$Economy [verbosity, destination] | Sends either a link or a series of links of economic updates to the "
        "destination, either 'channel', or 'dm'.\n "
    )
    await ctx.author.create_dm()
    await ctx.author.send(response)


@bot.command(name="Advice")
async def advice_alert(ctx, disaster_type):
    if disaster_type == "flood":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
    elif disaster_type == "fire":
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
    elif disaster_type == "all":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
        egg=random.randrange(1, 100)
        if egg >= 98:
            await ctx.send("If you hear someone announce that 'Monarch is active', stay low and hope you're on their side")
        else:
            await ctx.send("Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")
    else:
        await ctx.send("Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")


@bot.command(name="party_cleanup")
async def clean_after_time(ctx):
    """A blind function that clears a channel of all messages from a specific time or message id."""
    await ctx.channel.purge(after="2020-04-30 05:01:00.000+00:00")
    print("messages deleted")





@bot.command(name="MoveOn")
async def move_apartment(ctx):
    await ctx.send("Terminating epistemological fields, unbinding existing contacts. Mind seal broken.")


@bot.command(name="playlist_me")
async def need_tunes_bro(ctx):
    await ctx.send("I've got you, sending you some Rhythm bot commands in a DM now!")
    await ctx.author.create_dm
    await ctx.author.send("Here are the commands for this year's Triple J Hottest 100. I hope it helps.")
    with open("TripleJ-Hot100-2020.txt", "r") as tunes:
        for song in tunes:
            await ctx.author.send(song)
        egg = random.randrange(1, 100)
        if egg >= 98:
            await ctx.author.send("?play The Banshee Queen, The Daughter Who Died")


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger.addHandler(handler)

bot.run(TOKEN)
