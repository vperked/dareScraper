import json
import sys
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.utils import find_connectable_ip
from functions import database

class Setup:  ## Contains methods for setting up DareScraper.
    @staticmethod
    def ifRoot():
        # Check if the script is being run as root (user ID 0)
        if os.getuid() == 0:
            Messages.Errors.errorMessage("Please run in user mode!")
            sys.exit()  # Exit if root
          
    @staticmethod
    def aptUpdate():
        try:
            print("Updating your system packages...")
            cmd = subprocess.run(["sudo", "apt", "update"])  ## Run command on linux machine to update package list
            if cmd.returncode == 0:
                print(f"Done updating, upgrading now...")
                return Setup.aptUpgrade()  # Proceed to upgrade if update is successful
            else:
                sys.exit()  # Exit if update fails
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle errors
            return False

    @staticmethod
    def aptUpgrade():
        try:
            print("Now upgrading system packages...")
            cmd = subprocess.run(["sudo", "apt", "upgrade", "-y"])  ## Run command on linux machine to upgrade packages
            if cmd.returncode == 0:
                print("Done upgrading")
                return True
            else:
                print("All programs are already up-to-date...")
            return True
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle errors
            return False

    @staticmethod
    def initConfig():
        try:
            # Load the website URL from the config.json file
            with open("config.json") as config:
                website = json.load(config)
                return website["website"]
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle errors

    @staticmethod
    def resolveWebsite():
        try:    
            website = Setup.initConfig()  # Get the website URL from config
            resolvedIP = find_connectable_ip(website)  # Resolve IP address of the website
            if resolvedIP == None:
                return Messages.Errors.errorMessage("No IP found!")
            else:
                return resolvedIP
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle errors

    @staticmethod
    def initGoogleCrawler():
        try:
            # Set up options for Chrome to run headlessly
            options = Options()
            argumentArray = ["--headless", "--disable-gpu", "--disable-blink-features=AutomationControlled"]
            for arg in argumentArray:
                options.add_argument(arg)  # Add arguments for headless browsing
            chromeDriver = webdriver.Chrome(options=options)  # Initialize Chrome WebDriver
            print("Chrome Driver Initialized, continuing...")
            return chromeDriver
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle errors

    @staticmethod
    def initFireFoxCrawler():
        try:    
            # Set up options for Firefox to run headlessly
            options = Options()
            options.add_argument("--headless")  # Headless mode for Firefox
            fireFoxDriver = webdriver.Firefox(options=options)  # Initialize Firefox WebDriver
            print("Firefox Driver Initialized, continuing...")
            return fireFoxDriver
        except Exception as e:
            Messages.Errors.errorMessage(error=e)  # Handle errors

    @staticmethod
    def startUp(driverChoice):
        # Start crawling based on user choice (Chrome or Firefox)
        if driverChoice == "c":  # If user chose Chrome
            chromeDriver = Setup.initGoogleCrawler()  
            Crawling.beganGoogleCrawling(chromeDriver)
        elif driverChoice == "f":  # If user chose Firefox
            fireFoxDriver = Setup.initFireFoxCrawler()  
            Crawling.beganfireFoxCrawling(fireFoxDriver)

class Crawling:  # Contains the actual crawling functionality.
    @staticmethod 
    def takeScreenShot(fireFoxDriver):
        # Take a screenshot of the current webpage if user chooses
        answer = input("Take a picture of page[y or n]:")
        if answer == "y":
            print("Taking screenshot of webpage")
            fireFoxDriver.get_full_page_screenshot_as_file("screenshot.png")  # Save screenshot
            return True
        else:
            return False

    @staticmethod
    def crawlFireFox(fireFoxDriver):
        try:
            # Crawl the website using the Firefox driver
            fireFoxDriver.get(Setup.initConfig())  # Navigate to the website
            fireFoxDriver.set_page_load_timeout(5)  ## Set page load timeout
            Crawling.takeScreenShot(fireFoxDriver)  ## Take a screenshot?
            ip = Setup.resolveWebsite()  # Resolve website's IP address
            if ip is None:
                print("No IP found.")
            elif ip == str:
                print(ip)
            return True
        except InvalidArgumentException as invalidDomain:  # Handle invalid domain
            Messages.Errors.errorMessage(f"Invalid Domain: {invalidDomain}.")
        except Exception as e:  ## Catch other errors
            Messages.Errors.errorMessage(error=e)
            return False  ## Return false if crawling fails

    @staticmethod
    def crawlGoogle(googleDriver):
        try:
            # Crawl the website using the Google Chrome driver
            googleDriver.get(Setup.initConfig())
            googleDriver.set_page_load_timeout(3)  # Set page load timeout
            ip = Setup.resolveWebsite()  # Resolve website's IP address
            if ip is None:
                print("No IP found.")
            elif ip == str:
                print(f"{ip} added to the DB.")
                database.Database.addToDataBase(ip=ip, redisConnection=database.Database.connectToDataBase())
            return True
        except InvalidArgumentException as invalidDomain:  # Handle invalid domain
            Messages.Errors.errorMessage(f"Invalid Domain: {invalidDomain}.")
        except Exception as e:  ## Catch other errors
            Messages.Errors.errorMessage(error=e)
            return False  ## Return false if crawling fails

    @staticmethod
    def beganGoogleCrawling(chromeDriver):
        # Begin crawling with Google Chrome
        result = Crawling.crawlGoogle(googleDriver=chromeDriver)
        if result:
            Messages.Errors.sucessMessage(Setup.initConfig())  # Send success message
            sys.exit()  # Clean exit
        else:
            print("Failed")

    @staticmethod
    def beganfireFoxCrawling(fireFoxDriver):
        # Begin crawling with Firefox
        result = Crawling.crawlFireFox(fireFoxDriver=fireFoxDriver)
        if result:
            Messages.Errors.sucessMessage(Setup.initConfig())  # Send success message
            sys.exit()  # Clean exit
        else:
            print("Failed!")

class Messages:
    class Errors:
        @staticmethod
        def errorMessage(error):
            # Print error message
            print(f"There was an error: {error}")
        @staticmethod
        def sucessMessage(website):
            # Print success message after crawling
            print(f"Crawled {website}")
        @staticmethod 
        def invalidJson():
            print("Please check config.json!")

if __name__ == "__main__":
    try:
        Setup.ifRoot()  # Ensure the script is not run as root
        driverChoice = input("c(Chrome) or f(Firefox):")  # Prompt user for browser choice
        print("Starting DB...")
        database.Database.connectToDataBase()
        Setup.startUp(driverChoice)  # Start the crawling process
    except Exception as e:
        Messages.Errors.errorMessage(e)  # Handle any unexpected errors
