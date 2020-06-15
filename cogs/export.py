import spacy
from spacy import displacy
from discord.ext import commands
from discord.ext.commands import Context
import json
import discord

class Exporter(commands.Cog, name='Exporter'):
	"""A module for exporting data held in the package's JSON files 
	to specific services, views, or filetypes.
	"""

	# Define the initialisation routine to include loading the NLP library. 
	# Yes it should be an argument, no I don't care. 

	def __init__(self):
		nlp = spacy.load("en_core_web_md")


	# Define a command to return a spaCy dependency parse on a given number
	# of news or qfes file entries. Allow for only certain parts to be parsed.
	
	@commands.command(name=nlp_parse)
	async def depedency_parse(self, ctx: Context, file: str, items: int, title: bool, tease: bool, content: bool):
		"""
  		Take a news or alert metadata file and run a spaCy dependancy 
		parse on parts of the contents.
		"""
  		if file == "NRM.json":
			resource = "items"					# news file list uses "items"
			if title:
				title_var = "title"
			if tease:
				tease_var = "article_short_description"
			if content:
				content_var = "article_category"
		elif file == "fire_alerts.json":
			resource = "alerts"					# QFES file list uses "alerts"
			if title:
				title_var = "title"
			if tease:
				tease_var = "content"			# QFES alerts only have two content items
			if content:
				content_var = "content"

		# do some simple maths to invert the number of items passed as an argument
		# so that it can be used to run back from the end of the list of items

		items = items - (items*2)

		# open the ingested file and load the requested number of items

		with open(file, "r") as source:
			meta_block = json.load(source)
		meta_list = meta_block.get(resource)
		working_list = meta_list[items:]

		# Compile a list of docs from the items and element to send through
		# spaCy's dependency parser. Call the new list parse_list.

		parse_list = []
  
		for item in working_list:
			if title:
				parse_list.append(self.nlp(title_var))
			if tease:
				parse_list.append(self.nlp(tease_var))
			if content:
				parse_list.append(self.nlp(content_var))

		# parse the list of docs through the dependency parser. This process
		# may take a long time and use significant system memory. 

		displacy.serve(parse_list, style="dep", page=True,)