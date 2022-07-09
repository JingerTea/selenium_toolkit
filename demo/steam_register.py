from selenium_toolbox.webdriver.prep_undetect_webdriver import get_driver
from selenium.webdriver.common.by import By
from HLISA.hlisa_action_chains import HLISA_ActionChains
from selenium_toolbox.recaptcha.buster_captcha_solver import buster_captcha_solver

driver = get_driver(chrome=r"/usr/bin/google-chrome-beta",
                    version=104, headless=True)
action = HLISA_ActionChains(driver, browser_resets_cursor_location=False)

driver.get("https://store.steampowered.com/join")
# Show mouse
js = open(r"others/show_mouse.js").read()
driver.execute_script(js)

# Enter email
email = driver.find_element(By.XPATH, '//input[@name="email"]')
reenter_email = driver.find_element(By.XPATH, '//input[@name="reenter_email"]')
action.send_keys_to_element(email, "thisisabot@gmail.com")
action.send_keys_to_element(reenter_email, "thisisabot@gmail.com")
action.perform()

# Solve reCaptcha
buster_captcha_solver().solve(driver, action)

# Register account
i_agree_check = driver.find_element(By.XPATH, '//input[@name="i_agree_check"]')
create_account = driver.find_element(By.XPATH, '//button[@form="create_account"]')
action.move_to_element_outside_viewport(i_agree_check).click()
action.click(create_account)
action.perform()