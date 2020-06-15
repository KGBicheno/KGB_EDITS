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


	#TODO the $emergency_cog_status command should be a class method and should return the state of emergency level in the server location
	@commands.command()
	async def emergency_cog_status(self, ctx):
		"""Returns the current build-status of the cog"""
		ratio = random.randrange(35, 60)
		await ctx.send("The emergency module is building at " + str(ratio) + " per cent.")


	@commands.command()
	async def emergency_numbers(self, ctx, country):
		print(country)
		with open("/home/websinthe/sambashare/KGB_Golem/KGB_EDITS/cogs/Emergency_numbers.json", "r") as listing:
			rollodex = json.load(listing)
		i18_numbers = rollodex.get("items")
		send_msg = """My datasheet doesn't contain every country yet, but 112 is a common emergency telephone number that can be dialed free of charge from most mobile telephones and, in some countries, 
	fixed telephones in order to reach emergency services (ambulance, fire and rescue, police). Also, in Australia If you have a hearing or speech impairment and your life or property is in danger, you can 
	contact police, fire or ambulance on 106 directly through a TTY (also known as a teletypewriter or textphone)."""
		for numbers in i18_numbers:
			print("Currently parsing:")
			print(numbers.get("Country"))
			if numbers.get("Country") == country:
				ambulance = numbers.get("Ambulance")
				police = numbers.get("Police")
				fire = numbers.get("Fire")
				notes = numbers.get("Notes")
				send_one = "The emergency numbers for {} are {} for ambulance, {} for police, and {} for fire".format(country, ambulance, police, fire)
				send_two = "You may also need to use {} if the situation arises".format(notes)
				send_code = "```"
				send_msg = send_code + "\n" + send_one + "\n" + send_two + "\n" + send_code
				print("Round over")		
			await ctx.send(send_msg)

def setup(bot):
	bot.add_cog(Emergency(bot))
