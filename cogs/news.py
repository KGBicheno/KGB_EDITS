import asyncio
import json
import pprint
import urllib.request
from datetime import datetime
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
import pymongo
from bson.json_util import dumps
import discord
import spacy
from newscatcher import Newscatcher, urls 
# from bson.json_util import loads


# TODO Add these fuzzy search APIs for news topics and first aid (or at least investigate)
# http://www.bbc.co.uk/developer/technology/apis.html
# https://www.bloomberg.com/professional/support/api-library/
# https://developers.google.com/youtube


# TODO Research how to use classes to give secure control of the bot to future users
from discord.ext.commands import CommandInvokeError


class News(commands.Cog):
	"""A module containing the news-gathering and presentation capabilities Brook possesses."""

	def __init__(self, bot):
		self.bot = bot
		self.purpose = "news"
		self.nrm_spool_on = bool
		self.qfs_spool_on = bool
		self.bom_spool_on = bool
		self.nrm_spool_time = int
		self.qfes_spool_time = int
		self.bom_spool_time = int
		self.__set_spool_time__()




	# TODO Sit down and learn how class initialisation works and why __set_spool_time__ needed a decorator
	@classmethod
	def __set_spool_time__(cls):
		cls.nrm_spool_time = 60
		cls.qfes_spool_time = 60
		cls.bom_spool_time = 360
		return cls.nrm_spool_time, cls.qfes_spool_time, cls.bom_spool_time

	# TODO Find out if non __init__ class methods are called at initialisation
	@classmethod
	def __set_spool_state__(cls):
		cls.nrm_spool_on = False
		cls.qfes_spool_on = False
		cls.bom_spool_on = False
		return cls.nrm_spool_on, cls.qfes_spool_on, cls.bom_spool_on

	# TODO define a spool as its own class at some point.
	def __update_spool_state__(self, spool, *arg: bool):
		"""Takes a spool and a boolean to update the state of one of the cog's ingestion pipes."""
		assert arg == isinstance(arg, bool), "True or False, is the spool on? Keep it boolean please."
		if spool == self.nrm_spool_on:
			self.nrm_spool_on = arg
		elif spool == self.qfes_spool_on:
			self.qfes_spool_on = arg
		elif spool == self.bom_spool_on:
			self.bom_spool_on = arg

	# TODO Work out if giving each spool its own set and update functions/methods would be better
	def __update_spool_timing__(self, spool, time):
		"""Takes a spool and an integer representing seconds to update how often an ingestion pipe checks its target"""
		assert time == isinstance(time, int), "Please enter a whole integer for the number of seconds between checks"
		if spool == self.nrm_spool_time:
			self.nrm_spool_time = time
		elif spool == self.qfes_spool_time:
			self.qfes_spool_time = time
		elif spool == self.bom_spool_time:
			self.bom_spool_time = time

	# TODO Need an explicit way of returning spoolt state values to False if ingestion fall over
	@commands.command()
	async def spooling_status(self, ctx):
		"""Returns which services are currently pulling data from their sources."""
		spool_status = ("NRM: " + str(self.nrm_spool_on),
		                "QFES: " + str(self.qfes_spool_on),
		                "BOM: " + str(self.bom_spool_on))
		await ctx.send(spool_status)

	# TODO Update the other cogs to show something at least this meaningful with their status functions, maybe rewire them all
	@commands.command()
	async def news_cog_status(self, ctx):
		"""Returns the current build-status of the cog"""
		spool_times = str(self.nrm_spool_time) + ", " + str(self.qfes_spool_time) + ", " + str(self.bom_spool_time)
		await ctx.send("The news module is spooling at " + spool_times + " seconds per core, NQB notation.")

	# TODO Have the sources in $economy scraped into the gaming cog for use with the monopoly sub-bot's strategy perhaps?
	@commands.command()
	async def economy(self, ctx, verbosity, destination):
		"""Presents a reading recommendation or list depending on the verbosity flag -c|-v for concise or verbose. The destination flag -m sends the output to a DM instead of the context channel."""
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
		reading_list = [econ_100, econ_101, econ_102, econ_103, econ_104, econ_105, econ_106, econ_107, econ_108,
		                econ_109,
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

	# TODO $qfes_pull needs an output, badly. Urgently. I need to plug in the python libraries they built for geo-spatial recognition
	@commands.command()
	async def qfes_pull(self, ctx):
		"""Periodically checks the QFES Alerts and refills the container file if new alerts exist"""
		# Add this feed as well https://newsroom.psba.qld.gov.au/RSS/0
		await ctx.send("Pull-down loop initiating [QFES|RSS-feed|term-out:on]")
		while ctx.bot.is_ready():
			with open("fire_alerts.json", "r") as container:
				spark_dict = json.load(container)
			watch_url = 'https://www.qfes.qld.gov.au/data/alerts/bushfireAlert.xml'
			parse_xml_url = urlopen(watch_url)
			xml_page = parse_xml_url.read()
			soup_page = BeautifulSoup(xml_page, "lxml")
			alert_line = soup_page.findAll("entry")
			for get_feed in alert_line:
				if get_feed.id.string in spark_dict:
					print("prevented duplicate ID")
					break
				else:
					pprint(get_feed.title.string)
					article_title = get_feed.title.string
					print("Title: ", article_title)
					article_id = get_feed.id.string
					print("id: ", article_id)
					article_content = get_feed.content.string
					print("link: ", article_content)
					article_category = get_feed.category['term']
					print("category: ", article_category)
					article_published = get_feed.updated.string
					print("published: ", article_published)
					article_updated = get_feed.updated.string
					print("updated ", article_updated)
					spark_dict.get("items").append(
						dict(title=article_title, article_content=article_content, article_category=article_category,
						     article_id=article_id, article_published=article_published))
					with open('fire_alerts.json', "w") as data:
						json.dump(spark_dict, data, indent=2)
					print("Last QFES refill occurred at:", datetime.now().isoformat())
					await asyncio.sleep(100)

	nlp = spacy.load("en_core_web_md")

	# TODO $nrm_pull needs an output, urgently, and I need to decide between bare links and an embed
	# TODO I need to find out why $qfes_pull seems to ingest faster than $nrm_pull
	@commands.command()
	async def nrm_pull(self, ctx):
		"""Periodically checks the NRM Overwatch RSS and updates the container file if new articles exist"""
		# def aa(a):
		#	return lambda a: a if a is not None else "---"
		await ctx.send("Pull-down loop initiated [NRM|Overwatch|term-out:on]")
		nlp = spacy.load("en_core_web_md")
		while ctx.bot.is_ready():
			with open("NRM.json", "r") as container:
				news_dict = json.load(container)
			watch_url = 'https://www.qt.com.au/feeds/rss/kierans-overwatch-latest-list/'
			parse_xml_url = urlopen(watch_url)
			xml_page = parse_xml_url.read()
			soup_page = BeautifulSoup(xml_page, "lxml")
			yarn_list = soup_page.findAll("item")
			for get_feed in yarn_list:
				if get_feed.guid.string in news_dict:
					print("prevented duplicate ID")
					break
				else:
					pprint(get_feed.title.string)		#get_feed will be the 'data' arguement to DbIngest
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
					article_short_description = get_feed.short_description.string
					try:
						article_pic = get_feed.short_description.next_sibling['url']
					except TypeError:
						article_pic = "https://i.imgur.com/1yRp9ts.jpg"
					print("article_pic: ", article_pic)
					article_tags = TagList(nlp, str(article_title), article_description)
					news_dict.get("items").append({"title"                    : article_title,
					                               "article_date"             : article_pubdate,
					                               "article_link"             : article_link,
					                               "article_category"         : article_description,
					                               "article_guid"             : article_guid,
					                               "article_short_description": article_short_description,
					                               "article_pic"              : article_pic,
												   "article_tag_list"		  : article_tags,
					                               })
					with open('NRM.json', "w") as data:
						json.dump(news_dict, data, indent=2)
					print("Last NRM refill occurred at:", datetime.now().isoformat())
					await asyncio.sleep(20)


	@commands.command(hidden=True)
	async def bom_pull(self, ctx):
		"""Periodically checks for new BOM alerts and updates the container file if they exist"""
		await ctx.send("Pull-down loop initiated [BOM|RSS-feed|headers:explicit|term-out:on]")
		klaxon = []
		while ctx.bot.is_ready():
			self.bom_spool = 1
			with open("bom_alerts.json") as container:
				bom_alerts = json.load(container)
			bom_req = urllib.request.Request("http://www.bom.gov.au/fwo/IDZ00056.warnings_qld.xml",
			                                 data=None,
			                                 headers={
				                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"},
			                                 origin_req_host="123.211.133.33", unverifiable=True,
			                                 method="GET")
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
				print(bom_alerts)
			with open("bom_alerts.json", "w") as data:
				json.dump(bom_alerts, data, indent=2)
			await asyncio.sleep(360)

	@commands.command()
	async def style_guide(self, ctx, search_term=None):
		"""for a list of terms covered by the guide, invoke the style_list command"""
		if search_term is None:
			await ctx.send(
				"> The style_guide command allows you to search the News Corp style guide for specific word usages.\n"
				"> Invoke the command and then follow it with the word you're looking for."
				"""
				 ```css
				 [For example:] $style guide about 
				```""")
		else:
			assert isinstance(search_term, str)
		with open('NCA_style_guide.json', 'r', encoding='UTF-8') as reference:
			guide = json.load(reference)
			reference = guide['entries']
		for x in reference:
			for entry, answer in x.items():
				if entry == search_term:
					result = "Entry: " + entry + "  Ruling: " + answer
					await ctx.send(result)

	@commands.command()
	async def news(self, ctx):
		article_list = []
		with open("NRM.json", "r") as source:
			json_block = json.load(source)
		dict_list = json_block.get("items")
		article_1 = dict_list[-1]
		article_2 = dict_list[-2]
		article_3 = dict_list[-3]
		article_4 = dict_list[-4]
		article_5 = dict_list[-5]
		embed = discord.Embed(title="The Liquid Chronicle", url='https://www.buymeacoffee.com/KGBicheno',
		                      type="rich", description="News on demand, brought straight to your channel",
		                      color=0xff8000)
		embed.set_author(name="KGB_EDITS: Brook Newsly", url='https://www.patreon.com/KGBicheno',
		                 icon_url='https://i.imgur.com/KP6B8zx.png')
		embed.set_thumbnail(url='https://i.imgur.com/bQSgvV1.jpg')
		embed.add_field(name=article_1.get("title"), value=article_1.get("article_link"), inline=False)
		embed.add_field(name=article_2.get("title"), value=article_2.get("article_link"), inline=False)
		embed.add_field(name=article_3.get("title"), value=article_3.get("article_link"), inline=False)
		embed.add_field(name=article_4.get("title"), value=article_4.get("article_link"), inline=False)
		embed.add_field(name=article_5.get("title"), value=article_5.get("article_link"), inline=False)
		embed.set_image(url="https://i.imgur.com/1yRp9ts.jpg")
		embed.set_footer(
			text="""The news presented here has not been vetted for accuracy or lack of bias - yet. By contributing to 
	Kieran's Patreon you'll give him the time and resources to add the required technologies to Brook's code. 
	Backing him starts at as little as $3 a month — check it out here: https://www.patreon.com/KGBicheno""")
		await ctx.send(embed=embed)

	@commands.command(hidden=True)
	async def news_urls(self, ctx):
		aus_substring = ".au"
		blog_substring = "blog"
		
		english_urls = urls(language = 'en')
		pprint(english_urls)
		send_type = "The enlish_urls list registers as a {} python variable.".format(type(english_urls))
		send_len = "The overall list is {} urls long.".format(len(english_urls))
		send_aus = "Of those urls, {} contain .au somewhere.".format(len([i for i in english_urls if aus_substring in i]))
		send_blog = "Lastly, {} refer to themselves as a 'blog' in some way.".format(len([i for i in english_urls if blog_substring in i]))
		await ctx.send(send_type)
		await ctx.send(send_len)
		await ctx.send(send_aus)
		await ctx.send(send_blog)
		await ctx.send("The Australian-identifying urls are:")
		for i in english_urls:
			if ".au" in i:
				await ctx.send(i)

def TagList(nlp, arg, *arg2):
	
	print("arg: ", arg)
	print("arg2: ", arg2)

	description = str(arg2[0])

	
	taglist = []
	doc = nlp(arg)

	for token in doc:
		if token.pos_ == "PROPN":
			if token.text not in taglist:
				taglist.append(token.lemma_)
		elif token.is_stop == True:
			token = ""
		elif token.pos_ == "PRON":
			token = ""
		elif token.pos_ == "VERB":
			if token.text not in taglist:
				taglist.append(token.lemma_)
		elif token.pos_ == "NOUN":
			taglist.append(token.lemma_)
	if arg2 != None:
		doc2 = nlp(description)
		for token in doc2:
			if token.pos_ == "PROPN":
				if token.text not in taglist:
					taglist.append(token.lemma_)
			elif token.is_stop == True:
				token = ""
			elif token.pos_ == "PRON":
				token = ""
			elif token.pos_ == "VERB":
				if token.text not in taglist:
					taglist.append(token.lemma_)
			elif token.pos_ == "NOUN":
				if token.text not in taglist:
					taglist.append(token.lemma_)
	for tag in taglist:
		print(tag)
	return taglist




def setup(bot):
	bot.add_cog(News(bot))
