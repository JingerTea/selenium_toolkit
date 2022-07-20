import re
import seleniumwire.undetected_chromedriver as webdriver
from .proxy_options import proxy_options
import selenium_toolkit.reCaptcha as reCaptcha


def get_undetectable(profile=None, proxy=None, image=True,
                     chrome=None, version=None):
    """
    :param profile: Path of chrome profile. If profile does not exist, a new one will be created.
    :param proxy: Proxy address, supports HTTP/HTTPS/SOCKS5
    :param image: Chrome enable/disable image loading
    :param chrome: Path of chrome application
    :param version: Chrome version
    :return: Selenium driver
    """

    options = webdriver.ChromeOptions()
    seleniumwire_options = None
    # options.headless = True

    # Proxy
    if proxy:
        try:
            if "@" in proxy:
                str = re.match(r'(.*)://(.*):(.*)@(.*):(.*)', proxy)
                method = str.group(1)
                user = str.group(2)
                pwd = str.group(3)
                host = str.group(4)
                port = str.group(5)
                seleniumwire_options = proxy_options(method, host, port, user, pwd)
            else:
                str = re.match(r'(.*)://(.*):(.*)', proxy)
                method = str.group(1)
                host = str.group(2)
                port = str.group(3)
                seleniumwire_options = proxy_options(method, host, port)
        except:
            raise ValueError("Invalid Proxy, use format: method://user:pwd@host:port")

    # Profile
    if profile:
        options.add_argument(r'--user-data-dir=c:/temp/{profile}')

    # Download Buster Captcha Solver
    extn_1 = reCaptcha.get_buster(unzip=True)
    # Load extensions
    options.add_argument(f"--load-extension={extn_1}")

    # Chrome preference
    prefs = {}
    # Disable popup password
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    # Disable images
    if not image:
        prefs["profile.managed_default_content_settings.images"] = 2
    options.add_experimental_option("prefs", prefs)

    if chrome:
        options.binary_location = chrome

    chrome_driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options,
                                     use_subprocess=True, version_main=version)

    return chrome_driver


if __name__ == "__main__":
    driver = get_undetectable()
