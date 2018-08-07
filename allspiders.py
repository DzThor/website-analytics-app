import scrapy
import os
import os

class SpiderRunner:
    """Context manager for changing the current working directory through different spiders"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

    

def main():
    directoriesToVisit = ["spider_foller", "spider_keyhole", "spider_likealyzer", "spider_socialmention", "spider_tweetreach"]

    for directory in directoriesToVisit:
        with SpiderRunner(directory):
            os.system("scrapy crawl " + directory.replace("spider_",""))

if __name__ == "__main__":
    main()