from discord.ext import commands

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def setup(self, bot):
        bot.add_cog(GameCommands(bot))