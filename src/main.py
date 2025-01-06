from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
class Setup:
    def initCrawler():
        options = Options()
        options.add_argument("--headless") 
        fireFoxDriver = webdriver.Firefox(options=options)
        return fireFoxDriver
    def beganCrawling(fireFoxDriver):
        result = Crawling.crawlSite(fireFoxDriver=fireFoxDriver)
        if result == True:
            print("Done")
        else:
            print("Failed!")
class Crawling:
    def crawlSite(fireFoxDriver):
        try:
            fireFoxDriver.get("http://localhost:5000/api/ip")
            fireFoxDriver.set_page_load_timeout(5)
            return True
        except Exception as e:
            print(f"{e}")
            return False
    


if __name__ == "__main__":
    setup = Setup()
    driver = Setup.initCrawler()
    result = Setup.beganCrawling(driver)
    if result == False:
        driver.quit()

