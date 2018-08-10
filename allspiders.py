import os
import scrapy
import datetime
import pymongo

class SpiderRunner:
    """Context manager for changing the current working directory through different spiders"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def runSpiders():
    
    directoriesToVisit = [filename for filename in os.listdir('.') if filename.startswith("scrapy_")]
    
    starttime = " -a time=" + str(datetime.datetime.now().isoformat())
    for directory in directoriesToVisit:
        with SpiderRunner(directory):
            command = "scrapy crawl " + directory.replace("scrapy_","")
            print(command + starttime)
            os.system(command + starttime)


def main():

    runSpiders()

if __name__ == "__main__":
    main()
