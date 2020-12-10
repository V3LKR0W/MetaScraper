from pymongo import MongoClient
from keys import dbConnection, dbInfo

client = MongoClient(f'mongodb+srv://{dbConnection["username"]}:{dbConnection["password"]}@{dbConnection["cluster"]}/{dbConnection["dbname"]}?retryWrites=true&w=majority')



def addKey(key):
    db = client[dbInfo['name']]
    collection = db[dbInfo['collection']]
    
    payload = {
        'Key': str(key),
    }
    
    collection.insert(payload)
    
def checkKey(key):
    db = client[dbInfo['name']]
    collection = db[dbInfo['collection']]
    for result in collection.find({'Key':str(key)}):
        if result['Key'] == None:
            return None
        else:
            return 2

print(checkKey(''))
        