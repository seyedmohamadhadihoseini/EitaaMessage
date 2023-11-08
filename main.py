from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import helper
import os



def wait_until_present(bywath:By,name):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((bywath, name)))
        return element
    except :
        print("in wait_until function")

def get_contacts(driver):
    try:
        slidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-header')))
        slidebar=wait_until_present(By.CLASS_NAME,'sidebar-header')
        # slidebar=driver.find_element(By.CLASS_NAME,'sidebar-header')
        time.sleep(0.5)
        mybutton=slidebar.find_element(By.CLASS_NAME,'c-ripple')
        mybutton.click()
        menu_form=wait_until_present(By.CLASS_NAME,"tgico-user")
        # menu_form=driver.find_element(By.CLASS_NAME,"tgico-user")
        menu_form.click()
        contacts_form=wait_until_present(By.ID,"contacts")
        time.sleep(0.5)
        contacts=contacts_form.find_elements(By.TAG_NAME,"li")
        return contacts
    except Exception as e:
        print("in get content function")
        print(e)

def send_message(text):
    try:
        input_message=wait_until_present(By.CLASS_NAME,"input-message-input")
        input_message.send_keys(text)
        input_message.send_keys(Keys.RETURN)
    except:
        print("in sending message")
    
def get_toutal_message():
    try:
        all_chat=wait_until_present(By.CLASS_NAME,"bubbles-inner")
        time.sleep(0.5)
        messages_count=len(all_chat.find_elements(By.CLASS_NAME,"bubble-content-wrapper"))
        return messages_count
    except:
        print("in get total message")





driverPath="C:\\Program Files (x86)\\chromedriver.exe"
dOptions = webdriver.ChromeOptions()
dOptions.add_argument(f'--user-data-dir={os.path.join(os.getcwd(),"user_directory")}')

driver=webdriver.Chrome(driverPath)    

driver.get("https://web.eitaa.com/")      
try:
    h=helper.all_iterate(driver)
    h.run()

except Exception as e:
    print(e)
finally:
    pass
time.sleep(3*60)