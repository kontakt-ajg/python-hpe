from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#allow self-signed certificates
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True

#initialize browser
driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

##############
## Settings ##
login_url = "https://1.1.1.1"
login_username = "Administrator"
login_password = "myPassword"
##############

###########
## LOGIN ##
###########    

#visit login page in browser
driver.get(login_url)

#maximize the windows
#driver.maximize_window()

#set timeout for browser
login_wait = WebDriverWait(driver, 20)

#change to iframe with login fields
login_iframe = driver.find_element(By.CSS_SELECTOR, "#appFrame")
driver.switch_to.frame(login_iframe)

#enter username
login_username_field = login_wait.until(EC.element_to_be_clickable((By.ID, "username")))
login_username_field.clear()
login_username_field.send_keys(login_username)

#enter password
login_password_field = login_wait.until(EC.element_to_be_clickable((By.ID, "password")))
login_password_field.clear()
login_password_field.send_keys(login_password)

#press login button
login_button = login_wait.until(EC.element_to_be_clickable((By.ID, "login-form__submit")))
login_button.click()

#driver.close()