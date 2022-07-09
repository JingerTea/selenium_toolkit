import re
import seleniumwire.undetected_chromedriver as webdriver
from xvfbwrapper import Xvfb
from selenium_toolbox.recaptcha.buster_captcha_solver import buster_captcha_solver


def proxy_options(method, host: str, port: str,
                  user: str = None, password: str = None):
    if user and password:
        authentication = f"{user}:{password}@"
    elif not user and not password:
        authentication = ""
    else:
        raise ValueError("Proxy credentials are missing")

    if method == "http" or method == "https":
        method = ["http", "https"]
    elif method == "socks5":
        method = ["socks5", "socks5"]

    options = {
        "proxy": {
            "http": f"{method[0]}://{authentication}{host}:{port}",
            "https": f"{method[1]}://{authentication}{host}:{port}",
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    return options


def get_driver(profile=None,  proxy=None, image=True,
               chrome=None, version=None, headless: bool = False):

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
    extn_1 = buster_captcha_solver().download(unzip=True)
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

    if headless:
        vdisplay = Xvfb(width=1920, height=1080)
        vdisplay.start()
        options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options,
                              use_subprocess=True, version_main=version)

    return driver


if __name__ == "__main__":
    driver = get_driver()
