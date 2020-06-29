import json
from discord.ext import commands
import random
import discord


#TODO Add a rank or score to each member or team so they can be ranked
class Board(commands.Cog):
	"""The module for handling leaderboards"""

	def __init__(self, bot, name: str, seasonal: bool, team: bool, teams: list, members: list):
		self.bot = bot
		self.name = name
		self.seasonal = seasonal
		self.team = team
		self.teams = teams
		self.members = members
		self.season = 1

	def __repr__(self):
		string = "name \n"
		if self.team == True:
			for group in teams:
				string += group +"\n"
					for member in group:
						string += "\t" + member += \n
		elif self.team != True:
			for member in members:
				string += member
		return string

	@commands.command()
	def async add_team(self, ctx: Context, name: str)
		if self.team != True:
			await ctx.send("This board is for solo entrants only, please try add_name.")
		self.teams.append(dict(name = "name", members = []))
		response = ""

	@commands.command()
	def async add_team_member(self, ctx: Context, team:str, name: str)
		if self.team != True:
			await ctx.send("This board is for solo entrants only, please try add_name.")
		for group in self.teams:
			if team == self.teams.get('name')
				self.teams.get('members').append(name)
		response = "{} has been added to {} on leaderboard {}".format(name, team, self.name)
		await ctx.send(response)


	@commands.command()
	def async add_name(self, ctx: Context, name: str)
		if self.team == True"
			await ctx.send("This board is for team entrants only, please try add_team and add_team_member.")
		self.members.append(name)
		response = "{} has been added to leaderboard: {}".format(name, self.name)
		await ctx.send(response)

	@commands.command()
	def async reset_season(self)
		if self.team == seasonal
			self.teams = []
			self.members = []
			self.seasion += 1


	@commands.command()
	def async create_board(self, bot, name: str, seasonal: bool, team: bool, teams: list, members: list):
		newboard.name = name




def setup(bot):
	bot.add_cog(Board(bot))