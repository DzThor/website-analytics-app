import os
import scrapy
import datetime
import pymongo
import json
import time

class SpiderRunner:
    """Context manager for changing the current working directory """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def formatCommand(directory,starttime,searchName):
    base_command = "scrapy crawl"
    return " ".join([base_command, directory.replace("scrapy_",""), starttime, searchName])

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

    def itemExists(self,spiderDirectory,startTime,searchName):

        basetime = startTime.split("T")
        base = basetime[0]
        end = base + " 23:59:59.000"

        searchItem = {"source" : spiderDirectory.replace("scrapy_",""),
                      "date"   : {'$lt': datetime.datetime.strptime(end,self.dateformat)},
                      "name"   : searchName
                     }

        if(self.collection.find_one(searchItem)):
            return True
        else:
            return False

    def findAll(self):

        searchV = "Audi"
        stime = "2018-08-15 00:25:51.131"
        basetime = stime.split(" ")
        base = basetime[0]
        start = base + " 00:00:00.000"
        end = base + " 23:59:59.000"
        item = {"name" : searchV , "date" : {'$lt': datetime.datetime.strptime(end,self.dateformat)}}
        print(item)
        for element in self.collection.find(item):
            print(element)
            print('\n')



def prueba():

    dbchecker = DatabaseCheck()

    directoriesToVisit = [filename for filename in os.listdir('.') if filename.startswith("scrapy_")]
    stime = "2018-08-15T00:25:51.131"
    searchV = "Audi"
    #dbchecker.findAll()

    for directory in directoriesToVisit:
        print(directory)
        if(dbchecker.itemExists(directory,stime,searchV)):
            print("Si existe el elemento")
        else:
            print("Elemento no encontrado")

def caca():

    directoriesToVisit = [filename for filename in os.listdir('.') if filename.startswith("scrapy_")]
    actualtime = str(datetime.datetime.now().isoformat())
    starttime = "-a time=" + actualtime

    dbchecker = DatabaseCheck()

    with open('config.json', 'r') as f:
        config = json.load(f)

    searchParameter = "-a searchname=" + config['search']

    for directory in directoriesToVisit:

        if(dbchecker.itemExists(directory,actualtime,searchParameter)):
            break
        else:
            with SpiderRunner(directory) as spider:
                command = formatCommand(directory,starttime,searchParameter)
                print(command)
                x = os.system(command)
            if(dbchecker.itemExists(directory,actualtime,searchParameter)):
                print('\n')
                print(directory)

def main():

    directoriesToVisit = [filename for filename in os.listdir('.') if filename.startswith("scrapy_")]
    starttime = "-a time=" + str(datetime.datetime.now().isoformat())


    with open('config.json', 'r') as f:
        config = json.load(f)


    for directory in directoriesToVisit:
        for searchValue in config['SEARCH']:
            searchParameter = "-a searchname=" + searchValue
            with SpiderRunner(directory):
                command = formatCommand(directory,starttime,searchParameter)
                print(command)
                os.system(command)

if __name__ == "__main__":
    main()



