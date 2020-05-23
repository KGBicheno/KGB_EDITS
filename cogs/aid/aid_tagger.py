import os
import spacy
import json
from pprint import pprint

print("Loading spaCy core file ...")
nlp = spacy.load("en_core_web_md")
print("Core NLP file loaded.")

with open("AID.json", "r") as index:
	tag_index = json.load(index)
	print(tag_index['title'])

directory = r'/home/websinthe/sambashare/KGB_Golem/KGB_EDITS/cogs/aid/'

for filename in os.listdir(directory):
	print(filename)
	file_pdf = filename.replace(".txt", ".pdf", 1)
	if filename.endswith(".txt"):
		taglist = []
		with open(filename, "r") as source:
			document = source.read()
		doc = nlp(document)
		for token in doc:
			if token.pos_ == "PROPN":
				if token.text not in taglist:
					taglist.append(str(token.lemma_))
			elif token.is_stop == True:
				token = ""
			elif token.pos_ == "PRON":
				token = ""
			elif token.pos_ == "VERB":
				if token.text not in taglist:
					taglist.append(str(token.lemma_))
			elif token.pos_ == "NOUN":
				taglist.append(str(token.lemma_))
		for tag in taglist:
			tag_to_file = dict(tag=tag, file=file_pdf)
			pprint(tag_to_file)
			tag_index.get('items').append(tag_to_file)
			
with open("AID.json", "w") as update:
	json.dump(tag_index, update, indent=2)