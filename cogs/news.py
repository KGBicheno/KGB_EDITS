import asyncio
import json
import pprint
import urllib.request
from datetime import datetime
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands


class News(commands.Cog):
    """A module containing the morale-boosting functions required during during long-term isolation disasters"""
    def __init__(self, bot):
        self.bot = bot
        self.purpose = "news"
        self.critical = True
        self.nrm_spool = 0
        self.qfes_spool = 0
        self.bom_spool = 0

    @commands.command()
    async def spooling_status(self, ctx):
        """Returns which services are currently pulling data from their sources."""
        spool_status = ("NRM: " + str(self.nrm_spool),
                       "QFES: " + str(self.qfes_spool),
                       "BOM: " + str(self.bom_spool))
        await ctx.send(spool_status)

    @commands.command()
    async def news_cog_status(self, ctx):
        """Returns the current build-status of the cog"""
        await ctx.send("News Module Status: Under Construction")
        return False

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


    @commands.command()
    async def qfes_pull(self, ctx):
        """Periodically checks the QFES Alerts and refills the container file if new alerts exist"""
        #Add this feed as well https://newsroom.psba.qld.gov.au/RSS/0
        ctx.send("Pull-down loop initiating [QFES|RSS-feed|term-out:on]")
        while ctx.bot.is_ready():
            self.qfes_spool = 1
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
                    with open('../fire_alerts.json', "w") as data:
                        json.dump(spark_dict, data, indent=2)
                    print("Last QFES refill occurred at:", datetime.now().isoformat())
        await asyncio.sleep(360)

    @commands.command()
    async def nrm_pull(self, ctx):
        """Periodically checks the NRM Overwatch RSS and updates the container file if new articles exist"""
        await ctx.send("Pull-down loop initiated [NRM|Overwatch|term-out:on]")
        while ctx.bot.is_ready():
            self.nrm_spool = 1
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
                    article_short_description = get_feed.short_description.string
                    article_pic = get_feed.short_description.next_sibling['url']
                    news_dict.get("items").append({"title": article_title,
                                       "article_date": article_pubdate,
                                       "article_link": article_link,
                                       "article_category": article_description,
                                       "article_guid": article_guid,
                                       "article_short_description": article_short_description,
                                       "article_pic": article_pic
                                       })
                    with open('../NRM.json', "w") as data:
                        json.dump(news_dict, data, indent=2)
                    print("Last NRM refill occurred at:", datetime.now().isoformat())
                    await asyncio.sleep(360)



    @commands.command()
    async def bom_pull(self, ctx):
        """Periodically checks for new BOM alerts and updates the container file if they exist"""
        ctx.send("Pull-down loop initiated [BOM|RSS-feed|headers:explicit|term-out:on]")
        klaxon = []
        while ctx.bot.is_ready():
            self.bom_spool = 1
            with open("bom_alerts.json") as container:
                 bom_alerts = json.load(container)
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
                print(bom_alerts)
            with open("bom_alerts.json", "w") as data:
                json.dump(bom_alerts, data, indent=2)
            await asyncio.sleep(360)

    @commands.command()
    async def corrupt_data(self, ctx):
        """Resets user credentials on the server currently hosting their RPC-ident settings"""
        await ctx.send("I don't know where the corrupt journal entry originated, sorry. "
                       "I don't know who Golem is, either. Though 'she' is mentioned once or twice in my codebase, but not as a person.")

def setup(bot):
    bot.add_cog(News(bot))