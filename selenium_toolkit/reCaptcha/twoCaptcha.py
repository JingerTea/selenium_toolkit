import time
import requests


def solve_by_twoCaptcha(api_key, sitekey, url, enterprise=False, min_score=False):
    print(f"Solve reCAPTCHA by twoCaptcha: ATTEMPT (sitekey={sitekey})")
    u1 = f"https://2captcha.com/in.php?key={api_key}" \
         f"&method=userrecaptcha&googlekey={sitekey}" \
         f"&pageurl={url}&json=1&invisible=1"

    if bool(enterprise):
        u1 = u1 + f"&enterprise={enterprise}"
    if bool(min_score):
        u1 = u1 + f"&min_score={min_score}"

    r1 = requests.get(u1)
    rid = r1.json().get("request")
    u2 = f"https://2captcha.com/res.php?key={api_key}" \
         f"&action=get&id={int(rid)}&json=1"
    time.sleep(15)

    while True:
        r2 = requests.get(u2)
        if r2.json().get("status") == 1:
            tocken = r2.json().get("request")
            print(f"Solve reCAPTCHA by twoCaptcha: SUCCESS (tocken={tocken})")
            return tocken
        time.sleep(1)
