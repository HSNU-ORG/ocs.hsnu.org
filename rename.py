import pymongo
from pymongo import MongoClient
con = MongoClient(host='localhost', port=27017)
db = con.HSNUorg
collection = db.test
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)
print(result.inserted_id)
