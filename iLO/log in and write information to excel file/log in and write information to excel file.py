from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter

###########
## TO DO ##
###########

# Information > Overview > Status - Figure out a way to get "Connect to HPE" info (cant use CSS SELECTOR because it is the same as IP Address)

##############
## Settings ##
##############

login_url = "https://1.1.1.1"
login_username = "Administrator"
login_password = "myPassword"
excel_workbook_name = "sample.xlsx"
excel_worksheet_name = "iLO"


###############
## FUNCTIONS ##
###############

#function that trys to locate key and retrieve value. if it fails it will skip the item
def try_to_get_info(mydict):
    my_result = {}
    for item in mydict:
        try:
            my_key = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, item))).text
            my_value = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, mydict[item]))).text
        except:
            print("element with name >> " + item + " << not found. skipping.")
        else:
            my_result[my_key] = my_value
    return my_result

#function that writes the dict result of try_to_get_info() into an excel file
def write_into_excel(mydict):
    # iterating through content list
    global row
    global column
    for key in mydict:
        # incrementing the value of row by one
        # with each iterations.
        row += 1
        # write operation perform
        worksheet.write(row, column+1, key)
        worksheet.write(row, column+2, mydict[key])


#####################################
## INFO LOOKUP DICT (CSS_SELECTOR) ##
#####################################

server_dashboard_dict = {
    '#product_name_display_label':'#product_name_label',
    '#server_name_display_label':'#server_name_label',
    '#host_OSversion':'#host_OSversion_label',
    '#system_rom_display_label':'#system_rom_label',
    '#system_rom_date_display_label':'#system_rom_date_label',
    '#backup_rom_date_display_label':'#backup_rom_date_label',
    '#serial_num_display_label':'#serial_num_label',
    '#product_id_display_label':'#product_id_label',
    '#uuid_display_label':'#uuid_label'
}

ilo_dashboard_dict = {
    '#ip_address_display_label':'#ip_address_label',
    '#ipv6_link_local_display_label':'#ipv6_link_local_label',
    '#ilo_name_display_label':'#ilo_name_label',
    '#dedicatedNicLink > strong':'#dedicated_network_label',
    '#sharedNicLink > strong':'#shared_network_label',
    '#virtualNicLink > strong':'#ilo_virtual_nic_label',
    '#license_display_label':'#license_label',
    '#ilo_fw_version_display_label':'#ilo_fw_version_label'
}

status_dashboard_dict = {
    '#server_health_display_label':'#server_health_label > span > span.status-icon-label',
    '#system_health_display_label':'#system_health_label > span > span.status-icon-label',
    '#self_test_display_label':'#self_test_label > span > span.status-icon-label',
    '#security_row > strong > a':'#iloSecurity > span > span.status-icon-label',
    '#power_display_label':'#power_label > span > span.status-icon-label',
    '#uid_led_display_label':'#uid_led_label > span > span.status-icon-label',
    '#platform_RASPolicy_display_label':'#platform_RASPolicy_label',
    '#tpm_status_display_label > span':'#tpm_status_label > span > span',
    '#tpm_type_display_label':'#module_type_label > span > span',
    '#sd_card_status_display_label':'#sd_card_label > span > span',
#    '#ip_address_display_label':'#ers_state_label > a > span',
    '#AMS_label':'#AMSValue > span > span.status-icon-label'
}


###########
## EXCEL ##
###########

#create excel workbook and create new worksheet
workbook = xlsxwriter.Workbook(filename=excel_workbook_name)
worksheet = workbook.add_worksheet(name=excel_worksheet_name)

# Start from the first cell.
# Rows and columns are zero indexed.
row = 0
column = 0

#############
## BROWSER ##
#############

#allow self-signed certificates
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True

#initialize browser
driver = webdriver.Chrome(desired_capabilities=desired_capabilities)


###########
## LOGIN ##
###########    

#visit login page in browser
driver.get(login_url)

#maximize the windows
driver.maximize_window()

#set timeout for browser
wait = WebDriverWait(driver, 20)

#change to iframe with login fields
login_iframe = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#appFrame")))
driver.switch_to.frame(login_iframe)

#enter username
login_username_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
login_username_field.clear()
login_username_field.send_keys(login_username)

#enter password
login_password_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
login_password_field.clear()
login_password_field.send_keys(login_password)

#press login button
login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-form__submit")))
login_button.click()

#################
## INFORMATION ##
#################

#get current page (where are we?)
current_page = wait.until(EC.visibility_of_element_located((By.ID, "tabsetTitleSpan")))
print(current_page.text)

#check if we are on the correct page
assert current_page.text == 'Information'

#switch to iframe where info content is located
information_iframe = wait.until(EC.visibility_of_element_located((By.ID, "iframeContent")))
driver.switch_to.frame(information_iframe)

# Information > Overview: get server infomration
server_dashboard_result = try_to_get_info(server_dashboard_dict)
print(server_dashboard_result)

# Information > Overview: get ilo infomration
ilo_dashboard_result = try_to_get_info(ilo_dashboard_dict)
print(ilo_dashboard_result)

# Information > Overview: get status infomration
status_dashboard_result = try_to_get_info(status_dashboard_dict)
print(status_dashboard_result)


#Information > Overview: write current menu location into excel file
worksheet.write(row, column, "Information")

#Information > Overview: write server infomration into excel file
row += 1
column += 1
worksheet.write(row, column, "Server")
write_into_excel(server_dashboard_result)

#Information > Overview: write ilo infomration into excel file
row += 1
worksheet.write(row, column, "iLO")
write_into_excel(ilo_dashboard_result)

#Information > Overview: write status infomration into excel file
row += 1
worksheet.write(row, column, "Status")
write_into_excel(status_dashboard_result)

#autofit columns in excel worksheet
worksheet.autofit()

#close worksheet
workbook.close()

#close browser
driver.close()