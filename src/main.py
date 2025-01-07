import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.utils import find_connectable_ip
class Setup: ## Contains things used for setting up dareScraper.
    ## If user chooses, use the Google Driver.
    def initConfig():
        with open ("config.json") as config:
            website = json.load(config)
            return website["website"]
    def resolveWebsite(website):
        try:    
            website = Setup.initConfig()
            return find_connectable_ip(website)
        except Exception as e:
            Messages.Errors.errorMessage(e)
    def initGoogleCrawler():
        try:
            options = Options() 
            argumentArray = ["--headless", "--disable-gpu", "--disable-blink-features=AutomationControlled" ]
            options.add_argument(argumentArray[0])
            options.add_argument(argumentArray[1])
            options.add_argument(argumentArray[2])
            chromeDriver = webdriver.Chrome(options=options)
            return chromeDriver
        except Exception as e:
            Messages.Errors.errorMessage(e) # if error return the message
    ## If user chooses, use the FireFox Driver.
    def initFireFoxCrawler(website):
        try:    
            options = Options()
            options.add_argument("--headless") # make it headless 
            fireFoxDriver = webdriver.Firefox(options=options)
            return fireFoxDriver
        except Exception as e:
            Messages.Errors.errorMessage(error=e) # if error, return message
    def startUp(chromeDriver, fireFoxDriver):
        while True:
            print("c for chrome, f for firefox.")
            uI = input("Welcome to DareScraper:") # Grab user input 
            try:    
                ui = str(uI)
            except:
                print("Invalid")
                return
            if uI == "c": ## if they respond with C
                Setup.initGoogleCrawler() ## Call the setup class & init the Google Driver.
                Crawling.beganGoogleCrawling(chromeDriver)
            elif uI == "f": ## if they respond with F
                Setup.initFireFoxCrawler(website=Setup.initConfig()) ## Call the setup class & init the FireFox Driver.
                Crawling.beganfireFoxCrawling(fireFoxDriver)
class Crawling: # Contains the actual crawling. 
    def crawlFireFox(fireFoxDriver):
        try:
            fireFoxDriver.get(Setup.initConfig()) # Get the website
            fireFoxDriver.set_page_load_timeout(5) ## set the page timeout
            Setup.resolveWebsite(website=Setup.initConfig())
            return True
        except InvalidArgumentException as invalidDomain: # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.") # Error Message
        except Exception as e: ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False ## if fails return false so program cannot contiune on.
    def crawlGoogle(googleDriver):
        try:
            googleDriver.get(Setup.initConfig())
            googleDriver.set_page_load_timeout(3) # same as above, just with a different driver.
            ip = Setup.resolveWebsite(website=Setup.initConfig())
            if ip == None:
                print("No IP found.")
            elif ip == str:
                print(ip)
            return True
        except InvalidArgumentException as invalidDomain: # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.") # Error Message
        except Exception as e: ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False ## if fails return false so program cannot contiune on.
    def beganGoogleCrawling(chromeDriver):
        result = Crawling.crawlGoogle(googleDriver=chromeDriver) # Actually call the function and began crawling
        if result == True:
            Messages.Errors.sucessMessage(Setup.initConfig()) ## Send sucess message.
            sys.exit() ## Uses sys exit for clean exiting
        else:
            print("Failed")
    def beganfireFoxCrawling(fireFoxDriver):
        result = Crawling.crawlFireFox(fireFoxDriver=fireFoxDriver) # same thing as above.
        if result == True:
            Messages.Errors.sucessMessage(Setup.initConfig())
            sys.exit()  # same as above
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
    chromeDriver = Setup.initGoogleCrawler()
    fireFoxDriver = Setup.initFireFoxCrawler(website=Setup.initConfig())
    Setup.startUp(chromeDriver, fireFoxDriver)

