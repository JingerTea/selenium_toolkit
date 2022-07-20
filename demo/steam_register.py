import selenium_toolkit.chromedriver as chromedriver
import selenium_toolkit.reCaptcha as reCaptcha
from selenium.webdriver.common.by import By
from HLISA.hlisa_action_chains import HLISA_ActionChains

driver = chromedriver.get_official(chrome=r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe",
                                   version=104)
action = HLISA_ActionChains(driver)

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
reCaptcha.solve_by_buster(driver, action)

# Register account
i_agree_check = driver.find_element(By.XPATH, '//input[@name="i_agree_check"]')
create_account = driver.find_element(By.XPATH, '//button[@form="create_account"]')
action.move_to_element_outside_viewport(i_agree_check).click()
action.click(create_account)
action.perform()
