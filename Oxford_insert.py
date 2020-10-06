import json
import pymongo
from pymongo import MongoClient

client = MongoClient('Mongodb://127.0.0.1:27017/')
db = client.Crowthorne
collection = db.Oxford

with open('NRM.json') as toolargefile:
	file_contents = json.load(toolargefile)

list_of_elements = file_contents.get('items')
posts = db.posts

for element in list_of_elements:
	post_id = posts.insert_one(element).inserted_id
	print(post_id)

print.list_collection_names()











