from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_toolbox.recaptcha.twoCaptcha_solver import twoCaptcha_solver
from selenium_toolbox.recaptcha.buster_captcha_solver import buster_captcha_solver

class imperva_solver:
    def __init__(self, driver):
        self.driver = driver

    def check(self):
        # Check if solved
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[@id='main-iframe']"))
            )
            imperva_exist = True

        except:
            imperva_exist = False

        return imperva_exist

    def by_twocaptcha(self, api_key, url):
        self.driver.switch_to.frame(0)
        sitekey = self.driver.find_element(By.XPATH, "//div[@class='g-recaptcha']")
        sitekey = sitekey.get_attribute("data-sitekey")
        # Get token from 2Captcha for reCAPTCHA.V2
        token = twoCaptcha_solver(
            api_key=api_key,
            sitekey=sitekey,
            url=url
        )
        # Submit reCAPTCHA token to Google
        self.driver.execute_script("onCaptchaFinished(arguments[0]);", token)

    def by_buster(self, action):
        self.driver.switch_to.frame(0)
        buster_captcha_solver().solve(self.driver, action, method=2)