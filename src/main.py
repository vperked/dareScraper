from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
class Setup: ## Contains things used for setting up dareScraper.
    ## If user chooses, use the Google Driver.
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
    def initFireFoxCrawler():
        try:    
            options = Options()
            options.add_argument("--headless") # make it headless 
            fireFoxDriver = webdriver.Firefox(options=options)
            return fireFoxDriver
        except Exception as e:
            Messages.Errors.errorMessage(error=e) # if error, return message
    def startUp(chromeDriver, fireFoxDriver):
            print("c for chrome, f for firefox.") 
            uI = input("Welcome to DareScraper:") # Grab user input 
            if uI == "c": ## if they respond with C
                Setup.initGoogleCrawler() ## Call the setup class & init the Google Driver.
                Crawling.beganGoogleCrawling(chromeDriver)
            elif uI == "f": ## if they respond with F
                Setup.initFireFoxCrawler() ## Call the setup class & init the FireFox Driver.
                Crawling.beganfireFoxCrawling(fireFoxDriver)
class Crawling: # Contains the actual crawling. 
    def crawlFireFox(fireFoxDriver):
        try:
            website = "https://github.com"
            fireFoxDriver.get(website) # Get the website
            fireFoxDriver.set_page_load_timeout(5) ## set the page timeout
            return True
        except InvalidArgumentException as invalidDomain: # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.") # Error Message
        except Exception as e: ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False ## if fails return false so program cannot contiune on.
    def crawlGoogle(googleDriver):
        try:
            website = "https://github.com"
            googleDriver.get(website)
            googleDriver.set_page_load_timeout(3) # same as above, just with a different driver.
            return True
        except InvalidArgumentException as invalidDomain: # if there is no domain, or it is invalid it will return invalid domain.
            Messages.Errors.errorMessage(f"Invalid Domain Dipshit: {invalidDomain}.") # Error Message
        except Exception as e: ## Normal shit
            Messages.Errors.errorMessage(error=e)
            return False ## if fails return false so program cannot contiune on.
    def beganGoogleCrawling(chromeDriver):
        result = Crawling.crawlGoogle(googleDriver=chromeDriver) # Actually call the function and began crawling
        if result == True:
            print("Sent")
        else:
            print("Failed")
    def beganfireFoxCrawling(fireFoxDriver):
        result = Crawling.crawlFireFox(fireFoxDriver=fireFoxDriver) # same thing as above.
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
    chromeDriver = Setup.initGoogleCrawler()
    fireFoxDriver = Setup.initFireFoxCrawler()
    Setup.startUp(chromeDriver, fireFoxDriver)

