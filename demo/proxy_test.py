from selenium_toolbox.webdriver.prep_undetect_webdriver import get_driver
from selenium.webdriver.common.by import By

driver = get_driver(chrome=r"/usr/bin/google-chrome-beta",
                    version=104)

driver.set_window_size(1920,1080)
size = driver.get_window_size()
print(size)