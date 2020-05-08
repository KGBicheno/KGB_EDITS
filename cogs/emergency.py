from re import split
import json
from discord.ext import commands
import random
import discord
from operator import itemgetter

#TODO Build out the Emergency class, there's scope for having subclasses for the different types of disasters
class Emergency(commands.Cog):
	"""The key module for handling disaster situations and for providing aid to human actors"""

	def __init__(self, bot):
		self.bot = bot
		self.purpose = "emergency"
		self.critical = True

	#TODO the $emergency_cog_status command should be a class method and should return the state of emergency level in the server location
	@commands.command()
	async def emergency_cog_status(self, ctx):
		"""Returns the current build-status of the cog"""
		ratio = random.randrange(35, 60)
		await ctx.send("The emergency module is building at " + str(ratio) + " per cent.")

	#TODO Fix the web server to the files are always available or find a better CDN - the redirect issue is killing $aid
	#TODO $aid needs the fuzzy search libraries built in as soon as possible - it's borderline useless right now
	#TODO You have multilingual versions of the fact sheets, geo-locate or make multilingual usage more streamline - yesterday
	@commands.command()
	async def aid(self, ctx, *, arg):
		"""Searches the St John's Ambulance First Aid guides for anything that matches the text passed into the function"""
		assert isinstance(arg, str), "I'm sorry, I can only help if you tell me your situation."
		await ctx.send("Please wait a moment while I check if I have any resources for the situation")
		circumstances = split("\s", arg)
		print(circumstances)
		#TODO Add a funnel layer to catch the broadest variation of synonyms to database entries.
		with open("first_aid.json", "r", encoding="UTF-8") as repo:
			resources = json.load(repo)
		solutions = resources['items']
		outcomes = []
		for circumstance in circumstances:
			print(circumstance)
			for solution in solutions:
				print(solution)
				print(type(solution))
				#TODO I know this is a hack, need to change for i18
				#TODO This just isn't picking up obvious matches
				if circumstance.lower() in solution['situation'].lower():
					print(solution['situation'])
					print(solution['url'])
					outcomes.append((solution['situation'], solution['url'], solution['language']))
					#TODO Mirror the St John's files on my server and add a 'pretty' layer for thumbnails
		await ctx.send("I may have found something.")

		new_order = [2, 0, 1, 3, 4, 5]
		results = [outcomes[i] for i in new_order]

		#TODO reintroduce the non-English languages in a future patch when you've figured out a more streamlined way to do this.
		for result in results:
			print(results)
			print(result)
			aid = str(result[0])
			print(aid)
			linkage = str(result[1])
			print(linkage)
			language = str(result[2])
			print(language)
			if language != "English":
				break
			else:
				embed = discord.Embed(title="First Aid Card", type="rich", url='https://stjohn.org.au/first-aid-facts',
				                      description="Based on your description, this is what my database has returned",
				                      color=0xff0000)
				embed.set_author(name="Brook Newlsy",
				                 url='https://discordapp.com/oauth2/authorize?client_id=695245576475902002&permissions=8&scope=bot',
				                 icon_url='https://i.imgur.com/bQSgvV1.jpg')
				embed.set_thumbnail(url='https://i.imgur.com/KP6B8zx.png')
				embed.add_field(name="Situation", value=aid, inline=True)
				embed.add_field(name="Reference",
				                value=linkage,
				                inline=True)
				embed.set_footer(text="Please find a medical professional immediately. I'm not medically trained.")
				await ctx.send(embed=embed)
		#TODO Geolocate for the guild region's emergency service's number.
		#TODO Read those on fuzzy text matching
			#https://www.datacamp.com/community/tutorials/fuzzy-string-python
			#https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe
			#https://pypi.org/project/fuzzysearch/
			#https://www.geeksforgeeks.org/fuzzywuzzy-python-library/
			#http://theautomatic.net/2019/11/13/guide-to-fuzzy-matching-with-python/



def setup(bot):
	bot.add_cog(Emergency(bot))
