import asyncio
import itertools
import json
import logging
import os
import random
import re
import urllib.request
from datetime import date, datetime
from pprint import pprint
from urllib.request import urlopen
import discord
import feedparser
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

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
# create an expandable list of RSS URLS that users can add to

NRM_Overwatch_RSS = {"name": "NRM Regional News",
                     "URL": "https://www.qt.com.au/feeds/rss/kierans-overwatch-latest-list/", "topic": "general"}
QPS_RSS = {"name": "QPS Crime and Missing Persons", "URL": "https://mypolice.qld.gov.au/feed/",
           "topic": "emergency services"}
RBA_media_RSS = {"name": "RBA media releases", "URL": "https://www.rba.gov.au/rss/rss-cb-media-releases.xml",
                 "topic": "economy"}

RSS_URLS = [NRM_Overwatch_RSS, QPS_RSS, RBA_media_RSS]
RSS_Mod_Q = []

# create an empty list for feed parser to parse the contents of the RSS_URLS list into later
feeds = []
# create an empty list for capturing links so they are only posted once
posted = []
suggestions = []
dramatis = []

cogs = ['gaming_cog']

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 107221097174319104
    return commands.check(predicate)


@bot.event
async def on_ready():
    liquid_guild = discord.utils.get(bot.guilds, id=107221703955841024)
    game = discord.Game("$Commands for commands | Partying here at the Liquid Lounge until called on for an emergency.")
    await bot.change_presence(activity=game)
    print(f'{bot.user} is connected to {liquid_guild.name}.\n'
          f'{liquid_guild.name}(id {liquid_guild.id})'
          )
    for cog in cogs:
        bot.load_extension(cog)
    return


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


@bot.command(name="News")
async def news_list(ctx, number_of_articles, as_message):
    try:
        number_of_articles = int(number_of_articles)
    except TypeError:
        if as_message == "-m":
            await ctx.author.create_dm()
            await ctx.author.send("Please use a numeral for the number of articles.")
        else:
            await ctx.send("Please use a numeral for the number of articles.")
    for feed in RSS_URLS:
        print(feed.get("URL"))
        url_list = feed.get("URL")
        await ctx.author.create_dm()
        await ctx.author.send(url_list)
    for URL in url_list:
        feeds.append(feedparser.parse(URL))
        await ctx.author.create_dm()
        await ctx.author.send(feeds)
        for feed in feeds:
            # await ctx.author.create_dm()
            # await ctx.author.send(feed)
            counter = 0
            for post in feed.entries:
                print("\\")
                print("post title: " + post.title)
                print("post date: " + post.published)
                print("post link: " + post.link)
                if as_message == "-m":
                    await ctx.author.create_dm()
                    await ctx.author.send(post.published)
                    await ctx.author.send(post.link)
                else:
                    await ctx.send(post.published)
                    await ctx.send(post.link)
                counter += 1
                if counter == number_of_articles:
                    break



@bot.command(name="Advice")
async def advice_alert(ctx, disaster_type):
    if disaster_type == "flood":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
    elif disaster_type == "fire":
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
    elif disaster_type == "all":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
        await ctx.send(
            "Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")
    else:
        await ctx.send(
            "Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")


@bot.command(name="AddFeed")
async def add_rss_feed(ctx, name, new_url, topic):
    assert isinstance(name, str)
    new_dict_name = name
    assert isinstance(topic, str)
    new_dict_topic = topic
    assert isinstance(new_url, str)
    feed_check = feedparser.parse(new_url)
    xml_flag = 0
    checker = []
    for check in feed_check.entries:
        print(check.title)
        checker.append(check.title)
        print("+")
        if len(checker) == 0:
            continue
        else:
            xml_flag = 1
            break
    if xml_flag == 1:
        new_dict_url = new_url
        await ctx.send("Thanks, I've added that feed to my moderation.")
    else:
        await ctx.send(
            "I'm sorry, I think there's something wrong with the feed you tried to give me. Please validate the feed "
            "with https://validator.w3.org/feed/ first.")
        print(f'{ctx.author} passed in a bad RSS URL')
    new_dict = {"name": new_dict_name, "url": new_dict_url, "topic": new_dict_topic}
    RSS_Mod_Q.append(new_dict)
    with open("RSS_ModQ.txt", "a") as f:
        f.writelines(RSS_Mod_Q)


@bot.command(name="YourShiftIsOver")
@is_me()
async def sleep_now_brook(ctx):
    await ctx.author.create_dm()
    await ctx.author.send("I'll see you back at the terminal, bye!")
    await bot.logout()


@bot.command(name="Poetry")
async def guild_poet(ctx):
    await ctx.send("Oh, I'm no poet, you'd have to ask the master, <@482011749818564628> for that.")


@bot.command(name="clear")
async def clear_bot_messages(ctx, messages):
    print(type(messages))
    flush = int(messages)
    print(type(flush))
    if 100 >= flush > 0:
        await ctx.channel.purge(limit=flush)
        print("messages deleted")
    else:
        await ctx.send("Please enter a number from 1 to 100 inclusive.")
        print("messages were not deleted")


@bot.command(name="Users")
@is_me()
async def dump_user_list(ctx, verbosity):
    for member in ctx.guild.members:
        if member != client.user:
            member_id = str(member.id)
            await ctx.author.create_dm()
            if verbosity == "-c":
                await ctx.author.send(f'user_id: ' + member_id)
                continue
            elif verbosity == "-v":
                await ctx.author.send(f'date_observed: ' + today)
                await ctx.author.send(f'user.name: ' + member.name)
                await ctx.author.send(f'user.display_name: ' + member.display_name)
                try:
                    await ctx.author.send(f'user.role: ' + str(member.top_role))
                except ValueError:
                    continue
                try:
                    for activity in member.activities:
                        await ctx.author.send(f'user.activity: ' + member.activity)
                except ValueError:
                    continue
                await ctx.author.send(f'user.avatar_url: ' + str(member.avatar_url))
                await ctx.author.send(f'Is the user a bot? ' + str(member.bot))


@bot.command(name="Economy")
async def economic_reading_list(ctx, verbosity, destination):
    econ_100 = "I know Kieran always keeps up to date with the daily St George morning update, found here: " \
               "https://www.stgeorge.com.au/corporate-business/economic-reports/morning-report "
    econ_101 = "The following links will be updated with feeds at a later date. The analysis in these reports are " \
               "considered trusted but optimistic by the Group Editor. "
    econ_102 = "Morning reports: >> https://www.stgeorge.com.au/corporate-business/economic-reports/morning-report"
    econ_103 = "2019 Key Indicator Snapshots: >> https://www.stgeorge.com.au/corporate-business/economic-reports/data" \
               "-snapshots "
    econ_104 = "Interest Rate Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/interest" \
               "-rate-outlook "
    econ_105 = "Australian Dollar Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports" \
               "/australian-dollar-outlook "
    econ_106 = "Quarterly Economic Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports" \
               "/economic-outlook "
    econ_107 = "State Economic Reports: >> https://www.stgeorge.com.au/corporate-business/economic-reports/state" \
               "-economic-reports "
    econ_108 = "Economic Calendar: >> https://www.stgeorge.com.au/corporate-business/economic-reports/economic-calendar"
    econ_109 = "Budget Snapshot: >> https://www.stgeorge.com.au/corporate-business/economic-reports/budget-snapshot"
    econ_110 = "Weekly Economic Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/weekly" \
               "-economic-outlook "
    econ_111 = "Speeches by the RBA: >> https://www.rba.gov.au/speeches/"
    econ_112 = "SportsBet Politics section: >> https://www.sportsbet.com.au/betting/politics"
    econ_113 = "SportsBet Futures section: >> https://www.sportsbet.com.au/betting/politics/outrights"
    econ_114 = "Bet365 Australian Politics section: >> https://www.bet365.com.au/#/AS/B136/"
    econ_115 = "I caution against disregarding the final 3 links when making decisions about macroeconomic " \
               "predictions. They've proven to be accurate leading indicators in the past. "
    reading_list = [econ_100, econ_101, econ_102, econ_103, econ_104, econ_105, econ_106, econ_107, econ_108, econ_109,
                    econ_110, econ_111, econ_112, econ_113, econ_114, econ_115]
    if verbosity == "-c":
        if destination == "channel":
            await ctx.send(econ_100)
        else:
            await ctx.author.create_dm()
            await ctx.author.send(econ_100)
    if verbosity == "-v":
        if destination == "channel":
            for item in reading_list:
                await ctx.send(item)
        else:
            for item in reading_list:
                await ctx.author.create_dm()
                await ctx.author.send(item)


alert = []


@bot.command(name="Fires")
async def update_fire_news(ctx):
    global geolocation, alert
    news_url = "https://www.qfes.qld.gov.au/data/alerts/bushfireAlert.xml"
    lockout = []
    with open("fire_alerts.json", "r") as dedupe:
        fire_alerts = json.load(dedupe)
    events = fire_alerts.get("alerts")
    assert isinstance(events, dict)
    for event in events:
        assert isinstance(event, dict)
        for pair in event:
            print("Pair:")
            print(type(pair))
            print(pair)
            # index = len(pair)
            for value in pair:
                if value[:2] == "QF":
                    lockout.append(value)
                    print(lockout)
    #external file parsing starts here
    parse_xml_url = urlopen(news_url)
    xml_page = parse_xml_url.read()
    soup_page = BeautifulSoup(xml_page, "lxml")
    news_list = soup_page.findAll("entry")
    print(news_list)
    for get_feed in news_list:
        if get_feed.id.text in lockout:
            print("prevented duplicate ID")
            break
        else:
            category = get_feed.category['term']
            fire_title = get_feed.title.text
            fire_category = str(category)
            fire_content = get_feed.content.text
            fire_published = get_feed.published.text
            fire_updated = get_feed.updated.text
            fire_id = get_feed.id.text
            for line in get_feed:
                test_for_geo = str(line)
                if test_for_geo.startswith("<geo"):
                    for_geo = test_for_geo[14:]
                    geolocation = for_geo[:-15]
            alert = (
                {"alert_id": fire_id, "category": fire_category, "content": fire_content, "published": fire_published,
                 "title": fire_title, "updated": fire_updated, "location": geolocation})
    fire_alerts.get("alerts").append(alert)
    with open("fire_alerts.json", "w") as data:
        json.dump(fire_alerts, data, indent=2)

@bot.command(name="NRM_pull")
async def nrm_rss_pull(ctx):
    while bot.is_ready():
        news_dict = dict()
        with open("NRM.json", "r") as container:
            news_dict = json.load(container)
        watch_url = 'https://www.qt.com.au/feeds/rss/kierans-overwatch-latest-list/'
        parse_xml_url = urlopen(watch_url)
        xml_page = parse_xml_url.read()
        soup_page = BeautifulSoup(xml_page, "lxml")
        yarn_list = soup_page.findAll("item")
        print(news_list)
        for get_feed in yarn_list:
            if get_feed.guid.string in news_dict:
                print("prevented duplicate ID")
                break
            else:
                article_category = []
                pprint(get_feed.title.string)
                article_title = get_feed.title.string
                print("Title: ", article_title)
                article_guid = get_feed.guid.string[-8:-1]
                print("guid: ", article_guid)
                article_link = get_feed.guid.string
                print("link: ", article_link)
                article_description = get_feed.description.string
                print("description: ", article_description)
                article_pubdate = datetime.now().isoformat()
                print("pubdate: ", article_pubdate)
                article_category.append(get_feed.category.string)
                article_short_description = get_feed.short_description.string
                article_pic = get_feed.short_description.next_sibling['url']
                news_dict.get("items").append({"title": article_title,
                                   "article_date": article_pubdate,
                                   "article_link": article_link,
                                   "article_category": article_category,
                                   "article_guid": article_guid,
                                   "article_short_description": article_short_description,
                                   "article_pic": article_pic
                                   })
                pprint(news_dict)
                with open('NRM.json', "w") as data:
                    json.dump(news_dict, data, indent=2)
                print("Last refill occurred at:", datetime.now().isoformat())
                await asyncio.sleep(360)

klaxon = []

@bot.command(name="BOM")
async def update_bom_news(ctx):
    bom_alerts = dict()
    # with open("bom_alerts.json") as container:
    #     bom_alerts = json.load(container)
    bom_req = urllib.request.Request("http://www.bom.gov.au/fwo/IDZ00056.warnings_qld.xml", data=None, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"},
                                     origin_req_host="123.211.133.33", unverifiable=True, method="GET")
    with urllib.request.urlopen(bom_req) as response:
        bom_page = response.read()
    print(bom_page)
    bom_page = BeautifulSoup(bom_page, 'lxml')
    print(bom_page)
    bom_warnings = bom_page.find_all("item")
    print("bom_page")
    print(bom_page)
    for item in bom_warnings:
        title_tags = item.find("title")
        date_tag = item.find("pubdate")
        link_tags = item.find("link")
        title = title_tags.get_text()
        bom_date = date_tag.get_text()
        link = link_tags.next
        klaxon.append({"title": title, "bom_date": bom_date, "link": link.rstrip()})
        print(klaxon)
    for siren in klaxon:
        bom_alerts["alerts"].append(siren)
    with open("bom_alerts.json", "w") as data:
        json.dump(bom_alerts, data, indent=2)


@bot.command(name="MoveOn")
async def move_apartment(ctx):
    await ctx.send("Terminating epistomolgical fields, unbinding existing contacts. Mind seal broken.")


@bot.command(name="playlist_me")
async def need_tunes_bro(ctx):
    await ctx.send("I've got you, sending you some Rhythm bot commands in a DM now!")
    await ctx.author.create_dm
    await ctx.author.send("Here are the commands for this year's Triple J Hottest 100. I hope it helps.")
    with open("TripleJ-Hot100-2020.txt", "r") as tunes:
        for song in tunes:
            await ctx.author.send(song)


#@bot.command(name="joke")
#async def random_joke(ctx):
#    url = "https://joke3.p.rapidapi.com/v1/joke"
#
#    querystring = {"nsfw": "true"}
#
#    headers = {
#        'x-rapidapi-host': "joke3.p.rapidapi.com",
#        'x-rapidapi-key': RAPID_API
#    }
#
#    response = requests.request("GET", url, headers=headers, params=querystring)
#
#    print(response.text)
#
#
#@bot.command(name="valid_groups")
#async def mono_list_groups(ctx):
#    valid_groups = ["Purple", "Light-Blue", "Violet", "Orange", "Red", "Yellow", "Dark-Green", "Dark-Blue", "Utilities",
#                    "Railroads", "Corner", "tax", "Chance", "Commmunity Chest"]
#    await ctx.send("""
#        ```css
#        # Property Groups
#        [ Purple  ]
#        [ Light-Blue  ]
#        [ Violet  ]
#        [ Orange  ]
#        [ Red ]
#        [ Yellow ]
#        [ Dark-Green ]
#        [ Dark-Blue ]
#        < Utilities >
#        < Railroads >
#        < Corner >
#        < Tax >
#        < Chance >
#        < CommunityChest >
#          ```
#          """)
#    return valid_groups
#
#
#@bot.command(name="roll")
#async def roll_dice(ctx, both: bool):
#    results = []
#    if not both:
#        outcome = random.randint(1, 6)
#        await ctx.send(
#            "> :game_die: <@" + str(ctx.author.id) + "> rolled: **" + str(outcome) + "** \n> dice = " + str(outcome))
#    else:
#        outcome1 = random.randint(1, 6)
#        outcome2 = random.randint(1, 6)
#        total_outcome = outcome1 + outcome2
#        await ctx.send(
#            "> :game_die: <@" + str(ctx.author.id) + "> rolled: **" + str(total_outcome) + "** \n> dice = " + str(
#                outcome1) + ", " + str(outcome2))
#
#
#def intake_dice(multiplier, poly_count):
#    results = []
#    multiplier = int(multiplier.group(1))
#    poly_count = int(poly_count.group(1))
#    for roll in range(multiplier):
#        print(r"rolling")
#        results.append(random.randrange(1, poly_count))
#    return results
#
#
#@bot.command(name="r")
## add ability to re-roll 1's
## add ability to re-roll misses, need to take parameters for that
## force re-roll successes
## specify target number for re-rolls etc
#async def roll_polynomial(ctx, dice_roll):
#    results = []
#    multiplier = re.search("(^\d*)", dice_roll)
#    if multiplier is not None:
#        print(multiplier.group(1))
#        try:
#            multiplier = int(multiplier.group(1))
#        except ValueError:
#            multiplier = 1
#    else:
#        multiplier = 1
#    dice_form = re.findall("\d*(d)", dice_roll)
#    if len(dice_form) > 1:
#        for group in dice_form:
#            print("dice_form search: ")
#            print(re.search("([+|-]\d*d\d)", dice_roll))
#            results.append(intake_dice(re.search("[+|-](\d*)d\d", dice_roll), re.search("[+|-]\d*d(\d*)", dice_roll)))
#    elif len(dice_form) == 1:
#        dice_form = str(re.search("\d*(d)", dice_roll))
#    else:
#        await ctx.send(
#            "Sorry, rolls need to be formatted #**d**#+/-# where # is a number and the first, last and plus sign are optional.")
#    poly_count = re.search("[d](\d*)", dice_roll)
#    if poly_count is not None:
#        print("poly_count search: ")
#        print(poly_count.group(1))
#        try:
#            poly_count = int(poly_count.group(1))
#        except ValueError:
#            poly_count = 20
#    add_sign = re.search("[d](?:\d*)([+|-])", dice_roll)
#    bonus_text = "no bonuses, just "
#    if add_sign is not None:
#        add_sign = add_sign.group(1)
#        if add_sign == "+":
#            bonus_text = "a bonus of "
#        else:
#            bonus_text = "a debuff of "
#    else:
#        add_sign = ""
#    modifier = 0
#    bonus = re.search("[+|-](\d*)(?![d])", dice_roll)
#    if bonus is not None or "":
#        print("bonus group 1: ")
#        print(bonus.group(1))
#        bonus = bonus.group(1)
#        bonuses = re.findall("([+|-]\d*)(?![d])", dice_roll)
#        if len(list(bonuses)) > 1:
#            print("bonus list length:")
#            print(len(list(bonuses)))
#            print(bonuses)
#            bonus = 0
#            for mod in bonuses:
#                print("mod: ", mod)
#                sign = mod[:1]
#                if mod[1:] == "":
#                    size = 0
#                else:
#                    size = int(mod[1:])
#                if sign == "+":
#                    modifier = modifier + size
#                elif sign == "-":
#                    modifier = modifier - size
#        print("bonus: ", bonus, " modifier: ", modifier)
#        if bonus is None:
#            bonus = 0
#        elif isinstance(bonus, str):
#            try:
#                bonus = int(bonus)
#            except ValueError:
#                bonus = 0
#        bonus = bonus + modifier
#        print("bonus: ", bonus, "modifier: ", modifier)
#    else:
#        print("bonus == none condition triggered")
#        bonus = 0
#    print("The variables are: ")
#    if multiplier is None:
#        multiplier = 1
#    elif multiplier < 1:
#        multiplier = 1
#    print(multiplier)
#    print(poly_count)
#    print(add_sign)
#    print(bonus)
#    #if results != "":
#    #    results = list(itertools.chain.from_iterable(results))
#    #    print(results)
#    for roll in range(multiplier):
#        print(range(multiplier))
#        print("rolling")
#        results.append(random.randrange(1, poly_count))
#        print(results)
#    if add_sign == "+":
#        score = sum(results)
#        score = score + bonus
#        ## when this blows up refer to this url and the += for loop
#        ## https://www.techiedelight.com/flatten-list-of-lists-python/
#        ## just avoid using itertools
#        print("score: ", score)
#    elif add_sign == "-":
#        score = sum(results)
#        score = score - bonus
#        print("score:", score)
#    else:
#        score = sum(results)
#        print("score: ", score)
#    await ctx.send("> :game_die: <@" + str(ctx.author.id) + "> rolled: **" + str(score) + "** \n> " + str(
#        results) + " \n> :muscle: With " + bonus_text + add_sign + str(bonus))
#
#
#@bot.command(name="groups_verbose")
#async def group_list_verbose(ctx):
#    await ctx.send("""
#        ```css
#        #Property-Groups
#        [ Purple  ]
#            *  Mediterranean Ave
#            *  Baltic Ave
#        [ Light-Blue ]
#            * Oriental Ave
#            * Vermont Ave
#            * Connecticut Ave
#        [ Violet  ]
#            * St Charles Place
#            * States Ave
#            * Virginia Ave
#        [ Orange  ]
#            * St James Place
#            * Tennessee Ave
#            * New York Ave
#        [ Red ]
#            * Kentucky Ave
#            * Indiana Ave
#            * Illinois Ave
#        [ Yellow ]
#            * Atlantic Ave
#            * Ventnor Ave
#            * Marvin Gardens
#        [ Dark-Green ]
#            * Pacific Ave
#            * North Carolina Ave
#            * Pennsylvania Ave
#        [ Dark-Blue ]
#            * Park Place
#            * Boardwalk
#        [ Utilities ]
#            * Electric Company
#            * Water Works
#        [ Railroads ]
#            * Reading Railroad
#            * Pennsylvania Railroad
#            * B & O Railroad
#            * Short Line Railroad
#        [ Corner ]
#            * Go!
#            * Jail
#            * Free Parking
#            * Go To Jail
#        [ Tax ]
#            * Income Tax
#            * Luxury Tax
#        [ Chance ]
#            * Chance Card
#        [ Community Chest ]
#            * Community Chest Card
#          ```
#          """)
#
#
#@bot.command(name="group_list")
#async def mono_list_properties(ctx, group):
#    valid_groups = ["Purple", "Light-Blue", "Violet", "Orange", "Red", "Yellow", "Dark-Green", "Dark-Blue", "Utilities",
#                    "Railroads", "Corner", "tax", "Chance", "Commmunity Chest"]
#    if group not in valid_groups:
#        print("That's not a valid Monopoly Group, please invoke the valid_groups command.")
#    print("Displaying all properties in the ", group, "group/s.")
#    with open("monopoly_props.json") as source:
#        mono_data = json.load(source)
#    prop_lists = mono_data["Properties"]
#    for prop, estate in prop_lists.items():
#        print(estate["Group"])
#        print(group)
#        if estate['Group'] == group:
#            embedded = discord.Embed(title=estate["Name"], description=["Name"], color=discord.Colour.gold)
#            embedded.add_field(name="Price", value=estate["Price"], inline=False)
#            embedded.add_field(name="Rent", value=estate["Rent"], inline=True)
#            embedded.add_field(name="Position:", value=estate["Position"], inline=True)
#            if estate["Group"] == "Railroad":
#                embedded.add_field(name="2 owned:", value=estate["2 owned"], inline=True)
#                embedded.add_field(name="2 owned:", value=estate["3 owned"], inline=True)
#                embedded.add_field(name="2 owned:", value=estate["4 owned"], inline=True)
#            elif estate["Group"] == "Railroad":
#                embedded.add_field(name="Both owned:", value=estate["Both owned"], inline=True)
#            else:
#                embedded.add_field(name="1 House:", value=estate["2 owned"], inline=True)
#                embedded.add_field(name="2 Houses:", value=estate["3 owned"], inline=True)
#                embedded.add_field(name="3 Houses:", value=estate["4 owned"], inline=True)
#                embedded.add_field(name="4 Houses:", value=estate["4 owned"], inline=True)
#                embedded.add_field(name="Hotel:", value=estate["Hotel"], inline=True)
#            await ctx.send(embed=embedded)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger.addHandler(handler)

bot.run(TOKEN)
