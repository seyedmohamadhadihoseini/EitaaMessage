from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from dotenv import load_dotenv
import os
import db_manager
load_dotenv()
class userCommunicationState:
    justHello=0
    requestedForAds=1
    rejected=2
    accepted=3
    sent=4
    
    
class eitaaUser:
    def __init__(self,id,state,all_message_count=0) -> None:
        self.id=id
        self.state=state
        self.all_message_count=all_message_count
    
class doIterate:
    def __init__(self,driver) -> None:
        self.driver=driver

    def wait_until_present(self,bywath:By,name):
        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((bywath, name)))
            return element
        except :
            print("in wait_until function")
    def wait_until_present_sub(self,parent,bywath:By,name):
        try:
            wait = WebDriverWait(parent, 10)
            element = wait.until(EC.presence_of_element_located((bywath, name)))
            return element
        except :
            print("in wait_until function")
    def wait_until_presents(self,bywath:By,name,parent=None):
        try:
            if(parent is None):
                parent=self.driver
            
            wait = WebDriverWait(parent, 10)
            elements = wait.until(EC.presence_of_all_elements_located((bywath, name)))
            return elements
        except :
            print("in wait_until function")

    def get_contacts(self):
        while True:
            try:
                slidebar = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-header')))
                slidebar=self.wait_until_present(By.CLASS_NAME,'sidebar-header')
                # slidebar=driver.find_element(By.CLASS_NAME,'sidebar-header')
                time.sleep(0.5)
                
                mybutton = WebDriverWait(slidebar, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'c-ripple')))
                # mybutton=slidebar.find_element(By.CLASS_NAME,'c-ripple')
                mybutton.click()
                time.sleep(0.5)
                menu_form=self.wait_until_present(By.CLASS_NAME,"tgico-user")
                # menu_form=driver.find_element(By.CLASS_NAME,"tgico-user")
                menu_form.click()
                time.sleep(0.5)
                contacts_form=self.wait_until_present(By.ID,"contacts")
                time.sleep(1)
                contacts=self.wait_until_presents(By.TAG_NAME,"li",contacts_form)
                return contacts
            except Exception as e:
                print("in get content function")
                print("try again...")

    def get_contact(self,indx):
        while True:
            try:
                slidebar = WebDriverWait(self.driver, 200).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-header')))
                slidebar=self.wait_until_present(By.CLASS_NAME,'sidebar-header')
                # slidebar=driver.find_element(By.CLASS_NAME,'sidebar-header')
                time.sleep(0.5)
                
                mybutton = WebDriverWait(slidebar, 200).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'c-ripple')))
                # mybutton=slidebar.find_element(By.CLASS_NAME,'c-ripple')
                mybutton.click()
                time.sleep(0.5)
                menu_form=self.wait_until_present(By.CLASS_NAME,"tgico-user")
                # menu_form=driver.find_element(By.CLASS_NAME,"tgico-user")
                menu_form.click()
                time.sleep(0.5)
                contacts_form=self.wait_until_present(By.ID,"contacts")
                time.sleep(1)
                contact=self.wait_until_present_sub(contacts_form,By.CSS_SELECTOR,f'li:nth-child('+str(indx)+')')
                time.sleep(2)
                return contact
            except NoSuchElementException:
                return None
            except Exception as e:
                print("in get content function")
                print("try again")
                print(e)

    def send_message(self,text):
        try:
            input_message=self.wait_until_present(By.CLASS_NAME,"input-message-input")
            input_message.send_keys(text)
            input_message.send_keys(Keys.RETURN)
        except:
            print("in sending message")

    def isNewMessageArrived(self):
        try:
            time.sleep(2)
            all_chat=self.driver.find_elements(By.CLASS_NAME,"bubbles-date-group")
            lastMessage=all_chat[-1]
            time.sleep(0.5)
            lastDiv=lastMessage.find_elements(By.CLASS_NAME,"bubble")
            time.sleep(0.5)
            lastDiv=lastDiv[-1]
            attrs=lastDiv.get_attribute("class")
            if("is-in" in attrs):
                return True
            return False
            
            
        except:
            print("in get total message")
    def get_last_message(self)->str:
        messages=self.wait_until_presents(By.CLASS_NAME,"message")
        message=messages[-1]
        return message.text
    def find_element_by_text(self,elements,text,isInclude=True):
        for element in elements:
            if isInclude:
                if text in element.text:
                    return element
            else:
                if element.text==text:
                    return element
        return None
class all_iterate:
    def __init__(self,driver) -> None:
        self.dbManager=db_manager.db_manager()
        self.driver=driver
        self.doIterate=doIterate(driver)
        self.users=[]
        self.lastProgressIndex=0
        self.lastBucket=0
        self.contacts_count=int(os.getenv("contacts_count"))
 
        
    def newUpperBound(self):
        self.lastBucket= self.dbManager.getNewBucket()*int(os.getenv("contacts_count"))
        return self.lastBucket
        
    def send_hello_for_all(self,start,end):
        for i in range(start,end):
            contact=self.doIterate.get_contact(i)
            time.sleep(1)
            contact.click()
            time.sleep(0.5)
            self.doIterate.send_message("سلام")
            self.lastProgressIndex=i
            eitaa_user=eitaaUser(i,userCommunicationState.justHello)
            time.sleep(0.5)        
            self.users.append(eitaa_user)
            self.contacts_count-=1
            if(self.contacts_count<1):
                sleep_time=float(os.getenv("peiod_delay"))
                print(f"now i want to sleep for {sleep_time} seconds")
                
                time.sleep(sleep_time)
                self.contacts_count=int(os.getenv("contacts_count"))

  
    def is_user_accept_ads(self,msg):
        reject_list=["نه", "نفرست","نیازی نیست"]
        for word in reject_list:
            if word in msg:
                return userCommunicationState.rejected
        return userCommunicationState.accepted
    def send_ads(self):
        contact_name=self.doIterate.wait_until_present(By.CSS_SELECTOR,"div.person > div.content > div.top")
        time.sleep(0.5)
        contact_name=contact_name.text
     
        time.sleep(2)
        folder=self.doIterate.wait_until_present(By.ID,"folders-tabs")
        subFolders=self.doIterate.wait_until_presents(By.CLASS_NAME,"menu-horizontal-div-item")
        subFolder=self.doIterate.find_element_by_text(subFolders,"کانال")
        
        time.sleep(0.5)
        subFolder.click()
        time.sleep(0.5)
        chatlist=self.doIterate.wait_until_present(By.ID,"chatlist-container")
        time.sleep(0.5)
        
        chatlist=self.doIterate.wait_until_present_sub(chatlist,By.ID,"folders-container")
        time.sleep(0.5)
        chatlist=self.doIterate.wait_until_present_sub(chatlist,By.CLASS_NAME,"active")
        time.sleep(0.5)
        
        chatlist=self.doIterate.wait_until_present_sub(chatlist,By.CLASS_NAME,"chatlist-top")
        time.sleep(0.5)
        chatlist=self.doIterate.wait_until_present_sub(chatlist,By.CLASS_NAME,"chatlist")
        time.sleep(0.5)
        channelsList=chatlist.find_elements(By.TAG_NAME,"li")
        time.sleep(0.5)
        adschannel=self.doIterate.find_element_by_text(channelsList,os.getenv("ads_channel_name"))
        time.sleep(0.5)
        adschannel.click()
        time.sleep(0.5)
        lastMessage=self.doIterate.wait_until_presents(By.CLASS_NAME,"message")[-1]
        actions = ActionChains(self.driver)
        actions.context_click(lastMessage).perform()
        time.sleep(0.5)
        forward=self.doIterate.wait_until_present(By.CLASS_NAME,"tgico-forward-no-quote")
        time.sleep(0.55)
        forward.click()
        time.sleep(0.5)
        search_input=self.doIterate.wait_until_present(By.CLASS_NAME,"selector-search-input")
        time.sleep(1)
        search_input.send_keys(contact_name)
        time.sleep(0.5)
        contact_forward=self.doIterate.wait_until_present(By.CLASS_NAME,"popup-body")
        contact_forward=self.doIterate.wait_until_present_sub(contact_forward,By.CLASS_NAME,"chatlist")
        contact_forward=self.doIterate.wait_until_present_sub(contact_forward,By.TAG_NAME,"li")
        time.sleep(0.5)
        contact_forward.click()
        time.sleep(0.5)
        input_message=self.doIterate.wait_until_present(By.CLASS_NAME,"send")
        time.sleep(0.5)
        input_message.click()
        
        
        
    def checkForNewMessages(self,start,end):
        self.driver.refresh()
        time.sleep(4)
        i=start
        while i<end:     
                
            while(self.users[i].state==userCommunicationState.accepted or 
                  self.users[i].state==userCommunicationState.rejected):
                    i+=1
                    if(i>=end):
                        return
            
            contact=self.doIterate.get_contact(i+1)
            time.sleep(2.5)
            contact.click()
            time.sleep(1)
            if(self.doIterate.isNewMessageArrived()):
                if(self.users[i].state==userCommunicationState.justHello):
                    time.sleep(0.25)
                    self.doIterate.send_message("اجازه میدین که براتون یک پیام تبلیغاتی ارسال کنم؟")
                    time.sleep(0.5)
                    self.users[i].state=userCommunicationState.requestedForAds
                    
                elif(self.users[i].state==userCommunicationState.requestedForAds):
                    msg=self.doIterate.get_last_message()
                    self.users[i].state=self.is_user_accept_ads(msg)
                    if(self.users[i].state==userCommunicationState.accepted):
                        self.send_ads()
                self.contacts_count-=1
                if(self.contacts_count==0):
                    sleep_time=float(os.getenv("peiod_delay"))
                    print(f"now i want to sleep for {sleep_time} seconds")
                    time.sleep(sleep_time)
                    self.contacts_count=int(os.getenv("contacts_count"))
            i+=1
         
        self.driver.refresh()
    def manage_new_messages(self):
        for bucket in self.dbManager.history:
            print(self.dbManager.history)
            start=(bucket-1)*int(os.getenv("contacts_count"))
            end=bucket*int(os.getenv("contacts_count"))
            if(end>self.lastProgressIndex):
                end=self.lastProgressIndex
            self.checkForNewMessages(start,end)
    def manage_send_hello(self):
        time.sleep(2)
        contacts=self.doIterate.get_contacts()
        time.sleep(2)
        contacts_len=len(contacts)
        self.driver.refresh()
        time.sleep(5)
        if(self.lastProgressIndex>=contacts_len):
            return
        if(self.lastBucket!=0):
            if(contacts_len<=self.lastBucket-int(os.getenv("contacts_count"))):
                time.sleep(13)
                return
        end=self.newUpperBound()+1
        start=end-int(os.getenv("contacts_count"))
        if(end>contacts_len):
            end=contacts_len+1        
     
        self.send_hello_for_all(start,end)
    def run(self):
        while True:
            # check for contact counts
            self.manage_new_messages()
            self.manage_send_hello()
            
 