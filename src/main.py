from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
class Setup:
    def initGoogleCrawler():
        try:
            options = Options()
            arugementArray = ["--headless", "--disable-gpu", "--disable-blink-features=AutomationControlled" ]
            options.add_argument(arugementArray[0])
            options.add_argument(arugementArray[1])
            options.add_argument(arugementArray[2])
            chromeDriver = webdriver.Chrome(options=options)
            return chromeDriver
        except Exception as e:
            Messages.Errors.errorMessage(e)
    def initFireFoxCrawler():
        try:    
            options = Options()
            options.add_argument("--headless") 
            fireFoxDriver = webdriver.Firefox(options=options)
            return fireFoxDriver
        except Exception as e:
            Messages.Errors.errorMessage(error=e)
    def startUp(chrome, fireFox):
            print("c for chrome, f for firefox.")
            uI = input("Welcome to DareScraper:")
            if uI == "c":
                chrome = Setup.initGoogleCrawler()
            elif uI == "f":
                fireFox = Setup.initFireFoxCrawler()
class Crawling: 
    def crawlFireFox(fireFoxDriver):
        try:
            website = "https://github.com"
            fireFoxDriver.get(website)
            fireFoxDriver.set_page_load_timeout(5)
            return True
        except InvalidArgumentException as invalidDomain:
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.")
        except Exception as e:
            Messages.Errors.errorMessage(error=e)
            return False
    def beganCrawling(fireFoxDriver):
        result = Crawling.crawlSite(fireFoxDriver=fireFoxDriver)
        if result == True:
            print("Done")
        else:
            print("Failed!")
class WhenActive:
    def doThis():
        print("logic")
class Vaild:
    def isDomainValid():
        print("Logic")
class Messages:
    class Errors:
        def errorMessage(error):
            print(f"There was a error: {error}")
        def sucessMessage(website):
            print(f"Crawled {website}")

if __name__ == "__main__":
    Setup.startUp()

