#TODO MUSIC MODULE The music module needs to be built from the ground up with the following goals
#TODO MUSIC access music information about what's being played by other bots
#TODO MUSIC answer questions about music in general
#TODO MUSIC access digital radio stations from as many parts of the world as possible
#TODO MUSIC ingest as many digital radio signals as is possible given the hardware
#TODO MUSIC find new hardware for her to access to ingest new forms of digital and analogue radio signals
#TODO MUSIC pass that information back to the emergency and gaming modules to add to situational awareness


##TODO Make $playlist_me send a slightly more manageable chunk and make the output compatible with more bots
#@bot.command(name="playlist_me")
#async def need_tunes_bro(ctx):
#	await ctx.send("I've got you, sending you some Rhythm bot commands in a DM now!")
#	await ctx.author.create_dm
#	await ctx.author.send("Here are the commands for this year's Triple J Hottest 100. I hope it helps.")
#	with open("TripleJ-Hot100-2020.txt", "r") as tunes:
#		for song in tunes:
#			await ctx.author.send(song)