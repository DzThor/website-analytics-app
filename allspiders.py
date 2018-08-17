import os
import scrapy
import datetime
import pymongo
import json

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



def main():

    directoriesToVisit = [filename for filename in os.listdir('.') if filename.startswith("scrapy_")]
    starttime = "-a time=" + str(datetime.datetime.now().isoformat())


    with open('config.json', 'r') as f:
        config = json.load(f)

    searchParameter = "-a searchname=" + config['search']

    for directory in directoriesToVisit:
        with SpiderRunner(directory) as spider:
            command = formatCommand(directory,starttime,searchParameter)
            print(command)
            os.system(command)

if __name__ == "__main__":
    main()
