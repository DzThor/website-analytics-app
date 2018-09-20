twitter = { "followers": "lines",
               "averageLikesTwiiter": "lines",
               "averageRetweets": "lines",
               "accountsReached": "bars",
               "impressions": "bars",
               "tweetingSchedule": "bars",
               "averageEngRate": "percentage"
        }
from datetime import datetime,timedelta
import pymongo, json, pprint

def calcultateFirstDate(days):
    N = days
    return(datetime.now() - timedelta(days=N))

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def calculateDateSeries(initialDate):
    return  [dt.strftime("%m-%d") for dt in daterange(initialDate, datetime.now())]

def DateSeriesMongoDB(initialDate):
    return  [dt for dt in daterange(initialDate, datetime.now())]

def fillSeries(dateseries, db):
    print(dateseries[0])
    print(dateseries[-1])
    records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}})
    for i in records:
        print(i)
    print(records.count())

with open('config.json', 'r') as f:
    config = json.load(f)
    connection = pymongo.MongoClient(
        config['MONGODB_SERVER'],
        config['MONGODB_PORT']
    )
    db = connection[config['MONGODB_DB']]
    collection = db[config['MONGODB_COLLECTION']]
    names = config['SEARCH']

dateseries0 = '2018-08-30 13:03:28.522545'
dateseries1 = '2018-09-14 13:03:28.522545'
title = "followers"
records = collection.find({ "date": { '$gte': dateseries0, '$lt': dateseries1}},{"date" : 1, '_id' : False})
print(list(records))