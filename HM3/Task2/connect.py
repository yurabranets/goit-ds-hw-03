from filepath import path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

client=MongoClient(
    path,
            server_api=ServerApi('1')
)

db = client.HM

with open("authors.json", encoding="utf-8") as f:
    authors = json.load(f)

with open("quotes.json", encoding="utf-8") as f:
    quotes = json.load(f)

db.authors.insert_many(authors)
db.quotes.insert_many(quotes)