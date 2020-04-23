import feedparser
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

# today = date.today()
# print(f"today's date is {today}")
# print(f"The components of today's date are: {today.day} | {today.month} | {today.year}")

# print(datetime.now())

# time = datetime.time(datetime.now())
# print(time)

# wd = date.weekday(today)
# print(wd)
# days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
# print("Today is day number %d" % wd)
# print("Which is a ", days[wd])

# print(timedelta(days = 365, hours = 8, minutes = 15))
# print("today is", str(datetime.now()))
# print("One year from now it will be", str(datetime.now() + timedelta(days=365)))
# print("In one week and four days from now it will be", str(datetime.now() + timedelta(weeks=1, days=4)))

today = date.today()
nyd = date(today.year, 1, 1)
if nyd < today:
        print("New Years Day has already passed by %d now" % ((today - nyd).days))

primary_url="https://www.qt.com.au/feeds/rss/kierans-overwatch-latest-list/"
primary_url_alias = "Local News"

#create check_update() function
#passes URL of latest updated feed to parser```
#sets current_alias variable

#current_alias = (primary_url_alias)

#feed = feedparser.parse(primary_url)

#for post in feed.entries: #Only post entries made since previous request
        #print(current_alias)
        #print("post title: " + post.title)
        #print("post date: " + post.published)
        #print("post link: " + post.link)
        
#To-do
    # Set up PostgreSQL for Brook To store news entries. 
    # https://realpython.com/python-sql-libraries/#postgresql
    # Choose between JSON, XML, and Postgres for banter files