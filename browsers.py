
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import selenium.webdriver

import os
import sys
sys.path.append("..")

class DriverFactory:
    DriverType={'FIREFOX':1,'CRHOME':2}
    def __init__(self) -> None:
        
        pass
    def getDriver(self,drivertype:DriverType):
        if drivertype==1:   ## firefox
            service=Service(executable_path=r"D:\pyWorkspace\selenium\geckodriver.exe")
            options = FirefoxOptions()
            driver = selenium.webdriver.Firefox(service=service,options=options)
            return driver
        elif drivertype==2:   ## chrome
            service = Service(executable_path=r"D:\pyWorkspace\selenium\chromedriver.exe")
            options = ChromeOptions()
            driver = selenium.webdriver.Chrome(service=service,options=options)
            return driver
        else:
            print("Error for getDriver parameter, referring to usage: getDriver(1) for firefox, getDriver(2) for Chrome")
            return


    def installDriver(self,drivertype:DriverType):
        if drivertype==1: # firefox
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        elif drivertype==2: #chrome
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.utils import ChromeType
            driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        else:
            print("Error for getDriver parameter, referring to usage: installDriver(1) for firefox, installDriver(2) for Chrome")
            return
        

