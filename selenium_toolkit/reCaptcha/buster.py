import requests
import os
import zipfile
import time
import tempfile
from pathlib import Path
from random import randint
from selenium_toolkit.others.coordinate import coordinate
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_folder(path, notify=True):
    if not os.path.exists(path):
        os.makedirs(path)
        if notify:
            print(f"Check Folder: CREATE ({path})")
    else:
        if notify:
            print(f"Check Folder: EXIST ({path})")
    return path


def get_buster(unzip=False):
    url = "https://api.github.com/repos/dessant/buster/releases/latest"
    r = requests.get(url)

    # Chrome
    name = r.json()["assets"][0]["name"]
    dl_url = r.json()["assets"][0]["browser_download_url"]

    # Default directory
    directory = Path(tempfile.gettempdir())

    folder = create_folder(directory / "buster_captcha_solver_for_humans")
    path = folder / name

    if not os.path.exists(path):
        r = requests.get(dl_url, stream=True)
        with open(path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    if unzip:
        folder = os.path.splitext(path)[0]
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(folder)
        path = os.path.abspath(folder)
    else:
        path = os.path.abspath(path)
    return path


def check(driver, method: int = 1, frame=None) -> bool:
    """
    :param driver: Selenium webdriver
    :param method: Check status of reCaptcha
                   method=1: Check if reCaptcha is solved
                   method=2: Check if reCaptcha is existed
    :param frame: Parent frame of reCaptcha
    :return: (Bool) Status of reCaptcha
    """

    # Check if reCaptcha is solved
    if method == 1:
        try:
            # Switch to frame
            if frame:
                driver.switch_to.frame(frame)

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[@aria-checked='true']")))
            status = True
        except:
            status = False
        # Switch back to original frame
        if frame:
            try:
                driver.switch_to.parent_frame()
            except:
                pass

    # Check if reCaptcha is existed
    elif method == 2:
        try:
            # Switch to frame
            if frame:
                driver.switch_to.frame(frame)
            time.sleep(5)
            driver.find_element(By.XPATH, "//span[@aria-checked='false']")
            status = False
        except:
            status = True
        # Switch back to original frame
        if frame:
            try:
                driver.switch_to.parent_frame()
            except:
                pass
    else:
        raise ValueError("Invalid method")

    return status


def solve_by_buster(driver, action, method: int = 1):
    """
    :param driver: Pass in selenium webdriver
    :param action: Pass in HLISA Action Chain
    :param method: Define method to check status of reCaptcha
                   method=1: Check if reCaptcha is solved
                   method=2: Check if reCaptcha is existed
    :return: N/A
    """

    short_wait = randint(16413, 32708) / 10000
    long_wait = randint(47865, 71478) / 10000

    # Click reCaptcha Challenge
    frame1 = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']")))
    action.click(frame1).perform()

    time.sleep(short_wait)

    # Check if reCaptcha is solved
    status = check(driver, method, frame1)
    if status:
        print("reCpatcha is solved")
        return

    # Locate frame
    frame2 = driver.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")

    # Click "Get an audio challenge"
    driver.switch_to.frame(frame2)
    audio = driver.find_element(By.XPATH, "//button[@title='Get an audio challenge']")
    audio_xy = coordinate(driver, frame=frame2, element=audio).random()
    driver.switch_to.parent_frame()
    action.move_to(audio_xy['x'], audio_xy['y']).click().perform()

    time.sleep(short_wait)

    # Try solving reCaptcha
    for _ in range(3):
        # Locate frame again due to resize
        frame2 = driver.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")

        # Click buster "Solve the challenge"
        driver.switch_to.frame(frame2)
        buster = driver.find_element(By.XPATH, '//div[@class="button-holder help-button-holder"]')
        buster_xy = coordinate(driver, frame=frame2, element=buster).random()
        driver.switch_to.parent_frame()
        action.move_to(buster_xy['x'], buster_xy['y']).click().perform()

        time.sleep(short_wait)

        # Check if reCaptcha is solved
        status = check(driver, method, frame1)
        if status:
            print("reCpatcha is solved")
            return

        else:
            # Click "Get a new challenge"
            driver.switch_to.frame(frame2)
            refresh = driver.find_element(By.XPATH, '//button[@title="Get a new challenge"]')
            refresh_xy = coordinate(driver, frame=frame2, element=refresh).random()
            driver.switch_to.parent_frame()
            action.move_to(refresh_xy['x'], refresh_xy['y']).click().perform()
            time.sleep(long_wait)
