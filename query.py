import pymongo
import json

#connect to mongodb
myclient = pymongo.MongoClient("mongodb://root:cnmc@140.131.149.23:8080")
mydb = myclient["ocs"]
mycol = mydb["user"]

#filter with array include "國文": 0 ,"英文": 0 from mongodb and print it
myquery = { "國文": 80 ,"英文": 0 }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x) 
