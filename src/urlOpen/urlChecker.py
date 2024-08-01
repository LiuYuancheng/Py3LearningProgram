import os
import time
import keyboard
# change to use new webdriver-manager module : https://pypi.org/project/webdriver-manager/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from ConfigLoader import JsonLoader

#-----------------------------------------------------------------------------
class webActor(object):

    def __init__(self, driverPath=None) -> None:
        dirpath = os.path.dirname(__file__)
        chromeDriverPath = driverPath if driverPath else os.path.join(dirpath, 'chromedriver.exe')
        self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        #self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.startT = 0

    def openUrls(self, urlString):
        try:
            self.driver.get(urlString)
            time.sleep(2)
            keyboard.press_and_release('page down')
            time.sleep(0.1)
            keyboard.press_and_release('page down')
        except Exception as err:
            print('Ignore some internet not access exception %s' %str(err))
        time.sleep(2)
    
    def closeBrowser(self):
        self.driver.quit()


#-----------------------------------------------------------------------------
def main():
    loader = JsonLoader()
    loader.loadFile("urllist.json")
    client = webActor()
    for url in loader.getJsonData():
        client.openUrls(url)
    client.closeBrowser()

if __name__ == '__main__':
    main()
           