import random
import re
from discord.ext import commands

#TODO This Gaming module is a bit far down the list but consideration should be put into calling a limited instance of KGB_AFIRM in emergencies
class Gaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.purpose = "morale"
        self.critical = True

    #TODO $gaming_cog_status would be the perfect place to use the games analysis packages give a situation report to emergency workers
    @commands.command()
    async def gaming_cog_status(self, ctx):
        """Returns the current build-status of the cog"""
        ratio = random.randrange(35, 60)
        await ctx.send("The assent module is building at " + str(ratio) + " per cent.")

    #TODO $dice needs to be brought into a class or extension with the rest of the monopoly functions, consider getting a licence and releasing it
    @commands.command()
    async def dice(self, ctx , both: bool):
        if not both:
            outcome = random.randint(1, 6)
            await ctx.send("> :game_die: <@"+str(ctx.author.id)+"> rolled: **" + str(outcome) + "** \n> dice = " + str(outcome))
        else:
            outcome1 = random.randint(1, 6)
            outcome2 = random.randint(1, 6)
            total_outcome = outcome1 + outcome2
            await ctx.send("> :game_die: <@"+str(ctx.author.id)+"> rolled: **" + str(total_outcome) + "** \n> dice = " + str(outcome1) + ", " + str(outcome2))

    #TODO Delete the $hello command in gaming once I have a better structure for quickly checking for proper loads
    @commands.command()
    async def hello(self, ctx):
        print("Hello World!")
        await ctx.send("Hello World!")

    #TODO the $roll function needs to be the basis for the heavy-lifting of multivariate situational computation - fix its architecture asap, the regex needs to be perfect
    @commands.command()
    async def roll(self, ctx, dice_roll):
        await ctx.send("This roller is broken, use <@261302296103747584> instead for now.")
        results = []
        multiplier = re.search("(^\d*)", dice_roll)
        if multiplier is not None:
            #print(multiplier.group(1))
            try:
                multiplier = int(multiplier.group(1))
            except ValueError:
                multiplier = 1
        else:
            multiplier = 1      
        diceform = re.findall("[+|-]|\s|\d*(d)\d*|s|[+|-]", dice_roll)
        if len(diceform) > 0:
            print("At least one dice is present.")
        else:
            await ctx.send("Sorry, rolls need to be formatted #**d**#+/-# where # is a number and the first, last and plus sign are optional.")    
        poly_count = re.search("[d](\d*)", dice_roll)
        if poly_count is not None:
            #print("poly_count search: ")
            #print(poly_count.group(1))
            try:
                poly_count = int(poly_count.group(1))
            except ValueError:
                poly_count = 20
        add_sign = re.search("[d](?:\d*)([+|-])", dice_roll)
        bonus_text = "no bonuses, just "
        if add_sign is not None:
            add_sign = add_sign.group(1)
            if add_sign == "+":
                bonus_text = "a bonus of "
            else:
                bonus_text = "a debuff of "
        else:
            add_sign = ""
        modifier = 0
        bonus = re.search("[+|-](\d*)(?![d])", dice_roll)
        if bonus is not None or "":
            print("bonus group 1: ")
            print(bonus.group(1))
            bonus = bonus.group(1)
            bonuses = re.findall("([+|-]\d*)(?![d])", dice_roll)
            if len(list(bonuses)) > 1:
                print("bonus list length:")
                print(len(list(bonuses)))
                print(bonuses)
                bonus = 0
                for mod in bonuses:
                    print("mod: ", mod)
                    sign = mod[:1]
                    if mod[1:] == "":
                        size = 0
                    else:
                        size = int(mod[1:])
                    if sign == "+":
                        modifier = modifier + size
                    elif sign == "-":
                        modifier = modifier - size
            print("bonus: ", bonus, " modifier: ", modifier)
            if bonus is None:
                bonus = 0
            elif isinstance(bonus, str):
                try:
                    bonus = int(bonus)
                except ValueError:
                    bonus = 0
            bonus = bonus + modifier
            print("bonus: ", bonus, "modifier: ", modifier)
        else:
            print("bonus == none condition triggered")
            bonus = 0
        print("The variables are: ")
        if multiplier is None:
            multiplier = 1
        elif multiplier < 1:
            multiplier = 1
        print(multiplier)
        print(poly_count)
        print(add_sign)
        print(bonus)
        # if results != "":
        #    results = list(itertools.chain.from_iterable(results))
        #    print(results)
        for roll in range(multiplier):
            print(range(multiplier))
            print("rolling")
            results.append(random.randrange(1, poly_count))
            print(results)
        if add_sign == "+":
            score = sum(results)
            score = score + bonus
            ## when this blows up refer to this url and the += for loop
            ## https://www.techiedelight.com/flatten-list-of-lists-python/
            ## just avoid using itertools
            print("score: ", score)
        elif add_sign == "-":
            score = sum(results)
            score = score - bonus
            print("score:", score)
        else:
            score = sum(results)
            print("score: ", score)
        await ctx.send("> :game_die: <@" + str(ctx.author.id) + "> rolled: **" + str(score) + "** \n> " + str(
            results) + " \n> :muscle: With " + bonus_text + add_sign + str(bonus))


    #TODO The $monopoly command is designed to keep an isolated human occupied and sane, tighten up the code
    @commands.command()
    async def monopoly(self, ctx, info):
        if info == "help":
            await ctx.send("""
            The Monopoly command can be used to access information on the properties, rules, and status of the current game.
            The following arguments can be passed when the monopoly command is invoked:
            ```css
                - groups: presents a list of valid group names that can be searched using the 'monopoly search' command.
                    For example - $monopoly search Orange
                     ~~~ will return information on the three properties belonging to the Orange group.
                - properties: presents a list of valid property names that can be searched using the 'monopoly search' command.
                    For example - $monopoly search Boardwalk
                     ~~~ will return information on the property named Boardwalk
            ```
            """)
        elif info == "groups":
            await ctx.send("""
                ```css
                # Property Groups
                [ Purple  ]
                [ Light-Blue  ]
                [ Violet  ]
                [ Orange  ]
                [ Red ]
                [ Yellow ]
                [ Dark-Green ]
                [ Dark-Blue ]
                < Utilities >
                < Railroads >
                < Corner >
                < Tax >
                < Chance > 
                < Community Chest >
                ```
                """)
        elif info == "properties":
            await ctx.send("""
                ```css
                #Property-Groups
                [ Purple  ]
                    *  Mediterranean Ave
                    *  Baltic Ave
                [ Light-Blue ]
                    * Oriental Ave
                    * Vermont Ave
                    * Connecticut Ave
                [ Violet  ]
                    * St Charles Place
                    * States Ave
                    * Virginia Ave
                [ Orange  ]
                    * St James Place
                    * Tennessee Ave
                    * New York Ave
                [ Red ]
                    * Kentucky Ave
                    * Indiana Ave
                    * Illinois Ave
                [ Yellow ]
                    * Atlantic Ave
                    * Ventnor Ave
                    * Marvin Gardens
                [ Dark-Green ]
                    * Pacific Ave
                    * North Carolina Ave
                    * Pennsylvania Ave
                [ Dark-Blue ]
                    * Park Place
                    * Boardwalk
                [ Utilities ]
                    * Electric Company
                    * Water Works
                [ Railroads ]
                    * Reading Railroad
                    * Pennsylvania Railroad
                    * B & O Railroad
                    * Short Line Railroad
                [ Corner ]
                    * Go!
                    * Jail
                    * Free Parking
                    * Go To Jail
                [ Tax ]
                    * Income Tax
                    * Luxury Tax
                [ Chance ] 
                    * Chance Card
                [ Community Chest ]
                    * Community Chest Card
                  ```
                  """)
    

def setup(bot):
    bot.add_cog(Gaming(bot))
        