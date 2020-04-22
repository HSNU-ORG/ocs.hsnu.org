import pymongo
import json

#connect to mongodb
myclient = pymongo.MongoClient("mongodb://root:cnmc@140.131.149.23:8080")
mydb = myclient["ocs"]
mycol = mydb["user"]


#if the data didn't exist , insert it into data base
#there is only one disc in test.json
with open('test.json',encoding="utf-8") as f:
    file_data = json.load(f)
x = mycol.update_many(file_data, {'$set':file_data}, upsert=True)


