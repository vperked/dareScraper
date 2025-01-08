import json
import sys
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.utils import find_connectable_ip
class Setup:  ## Contains things used for setting up DareScraper.
    @staticmethod
    def aptUpdate():
        try:
            print("Updating your system packages...")
            cmd = subprocess.run(["sudo", "apt", "update"])
            if cmd.returncode == 0:
                print(f"Done updating, upgrading now...")
                return Setup.aptUpgrade()
            else:
                sys.exit()
        
        except Exception as e:
            Messages.Errors.errorMessage(e)
            return False
    @staticmethod
    def aptUpgrade():
        try:
            print("Now we upgrade...")
            cmd = subprocess.run(["sudo", "apt", "upgrade", "-y"])
            if cmd.returncode == 0:
                print("Done upgrading")
                return True
            else:
                print("All programs updated...")
            return True
        except Exception as e:
            Messages.Errors.errorMessage(e)
            return False
    @staticmethod
    def initConfig():
        try:
            with open("config.json") as config:
                website = json.load(config)
                return website["website"]
        except Exception as e:
            Messages.Errors.errorMessage(e)
    @staticmethod
    def resolveWebsite():
        try:    
            website = Setup.initConfig()
            return find_connectable_ip(website)
        except Exception as e:
            Messages.Errors.errorMessage(e)
    @staticmethod
    def initGoogleCrawler():
        try:
            options = Options() 
            argumentArray = ["--headless", "--disable-gpu", "--disable-blink-features=AutomationControlled"]
            options.add_argument(argumentArray[0])
            options.add_argument(argumentArray[1])
            options.add_argument(argumentArray[2])
            chromeDriver = webdriver.Chrome(options=options)
            print("Chrome Driver Initialized, continuing...")
            return chromeDriver
        except Exception as e:
            Messages.Errors.errorMessage(e)  # if error return the message
    @staticmethod
    def initFireFoxCrawler():
        try:    
            options = Options()
            options.add_argument("--headless")  # make it headless
            fireFoxDriver = webdriver.Firefox(options=options)
            print("Firefox Driver Initialized, continuing...")
            return fireFoxDriver
        except Exception as e:
            Messages.Errors.errorMessage(error=e)  # if error, return message
    @staticmethod
    def startUp(driverChoice):
            if driverChoice == "c":  # if they respond with C
                chromeDriver = Setup.initGoogleCrawler()  
                Crawling.beganGoogleCrawling(chromeDriver)
            elif driverChoice == "f":  # if they respond with F
                fireFoxDriver = Setup.initFireFoxCrawler()  
                Crawling.beganfireFoxCrawling(fireFoxDriver)
class Crawling:  # Contains the actual crawling.
    @staticmethod
    def crawlFireFox(fireFoxDriver):
        try:
            fireFoxDriver.get(Setup.initConfig())  # Get the website
            fireFoxDriver.set_page_load_timeout(5)  ## set the page timeout
            Setup.resolveWebsite()
            return True
        except InvalidArgumentException as invalidDomain:  # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.")  # Error Message
        except Exception as e:  ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False  ## if fails return false so program cannot continue on.
    @staticmethod
    def crawlGoogle(googleDriver):
        try:
            googleDriver.get(Setup.initConfig())
            googleDriver.set_page_load_timeout(3)  # same as above, just with a different driver.
            ip = Setup.resolveWebsite()
            if ip is None:
                print("No IP found.")
            elif ip == str:
                print(ip)
            return True
        except InvalidArgumentException as invalidDomain:  # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.")  # Error Message
        except Exception as e:  ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False  ## if fails return false so program cannot continue on.
    @staticmethod
    def beganGoogleCrawling(chromeDriver):
        result = Crawling.crawlGoogle(googleDriver=chromeDriver)  # Actually call the function and begin crawling
        if result:
            Messages.Errors.sucessMessage(Setup.initConfig())  # Send success message.
            sys.exit()  # Uses sys exit for clean exiting
        else:
            print("Failed")
    @staticmethod
    def beganfireFoxCrawling(fireFoxDriver):
        result = Crawling.crawlFireFox(fireFoxDriver=fireFoxDriver)  # same thing as above.
        if result:
            Messages.Errors.sucessMessage(Setup.initConfig())
            sys.exit()  # same as above
        else:
            print("Failed!")
class Messages:
    class Errors:
        @staticmethod
        def errorMessage(error):
            print(f"There was an error: {error}")

        @staticmethod
        def sucessMessage(website):
            print(f"Crawled {website}")
if __name__ == "__main__":
    try:
        driverChoice  = input("c or f:")
        print("Calling startup...")
        Setup.startUp(driverChoice)
    except Exception as e:
        Messages.Errors.errorMessage(e)
