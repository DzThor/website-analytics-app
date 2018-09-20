import pymongo, json, datetime
from random import randint

class DatabaseCheck:

    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            connection = pymongo.MongoClient(
                config['MONGODB_SERVER'],
                config['MONGODB_PORT']
            )
            db = connection[config['MONGODB_DB']]
            self.collection = db[config['MONGODB_COLLECTION']]
            self.dateformat = config['DATE_FORMAT']

    def createItem(self,date,source,platform):

        schedule = [['00', '4'],
                      ['01', '2'],
                      ['02', '4'],
                      ['03', '0'],
                      ['04', '0'],
                      ['05', '0'],
                      ['06', '0'],
                      ['07', '0'],
                      ['08', '0'],
                      ['09', '0'],
                      ['10', '0'],
                      ['11', '0'],
                      ['12', '43'],
                      ['13', '4'],
                      ['14', '6'],
                      ['15', '1'],
                      ['16', '15'],
                      ['17', '7'],
                      ['18', '4'],
                      ['19', '2'],
                      ['20', '0'],
                      ['21', '6'],
                      ['22', '4'],
                      ['23', '5']]


        item = { "date": datetime.datetime.strptime(date + " 01:00:01.100","%Y-%m-%d %H:%M:%S.%f"),
                 "name" : "Audi",
                 "source": source,
                 "platform": platform,
                 "followers": randint(1000000,2000000),
                 #"retweets": ,
                 "averageLikesTwiiter": randint(300,400),
                 "averageRetweets": randint(100,200),
                 "averageEngRate": randint(0,100),
                 "accountsReached": randint(1900000,2100000),
                 "impressions": randint(2000000,2200000),
                 "tweetingSchedule": schedule,
                 "totalPageLikes": randint(11000000,12000000),
                 "averageLikesFacebook": randint(3000,4000),
                 "averageComments": randint(40,120),
                 "averageShares": randint(200,300),
                 "averageEngagement": randint(0,100),
                 "peopleTalking": randint(30000,40000),
                 "frontPage": randint(0,100),
                 "activity": randint(0,100),
                 "about": randint(0,100),
                 "response": randint(0,100),
                 "engagement": randint(0,100),
                 "strength": randint(0,100),
                 "passion": randint(0,100),
                 "reach": randint(0,100),
                 "sentiment": randint(0,50)
                }

        return item

    def daterange(self,start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            print(start_date)
            yield start_date + datetime.timedelta(n)

def main():

    print("Hola")
    db = DatabaseCheck()
    start_date = datetime.date(2018,8,31)
    end_date = datetime.date(2018,9,30)
    print(start_date)
    platformsSource = { "keyhole_facebook" : "Facebook",
                        "keyhole_twitter" : "Twitter",
                        "foller" : "Twitter",
                        "likealyzer" : "Facebook",
                        "tweetreach" : "Twitter",
                        "socialmention" : "Internet"
    }
    print("empieza")
    for single_date in db.daterange(start_date, end_date):
        print("date")
        for source in platformsSource.keys():
            print("source")
            db.collection.insert_one(db.createItem(single_date.isoformat(), source,platformsSource.get(source)))
            print("bucle")
    print("acaba")
if __name__ == "__main__":
    main()