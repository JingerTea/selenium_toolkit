import re
from selenium_toolbox.recaptcha.buster_captcha_solver import buster_captcha_solver
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def proxy_options(method, host, port, user = None, password = None):
    if user and password:
        authetication = f"{user}:{password}@"
    elif not user and not password:
        authetication = ""
    else:
        raise ValueError("Proxy credentials are missing")

    if method == "http" or method == "https":
        method = ["http", "https"]
    elif method == "socks5":
        method = ["socks5", "socks5"]

    options = {
        "proxy": {
            "http": f"{method[0]}://{authetication}{host}:{port}",
            "https": f"{method[1]}://{authetication}{host}:{port}",
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    return options


def get_driver(profile=None,  proxy=None, image=True, chrome=None, version=None):
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

    driver = webdriver.Chrome(
        ChromeDriverManager(version=version).install(), options=options,
        seleniumwire_options=seleniumwire_options)

    return driver

if __name__ == "__main__":
    driver = get_driver()
