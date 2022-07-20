import selenium_toolkit.chromedriver as chromedriver
from selenium.webdriver.common.by import By

driver = chromedriver.get_official(chrome=r"/usr/bin/google-chrome-beta",
                    version=104)

driver.get("https://ip.oxylabs.io/")
