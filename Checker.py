from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
import itertools
from time import sleep
from explicit import waiter, XPATH


#set up chrome and navigate to instagram homepage
browser = webdriver.Chrome()
browser.implicitly_wait(1)
browser.get('https://www.instagram.com')
sleep(1)

##LOGIN##
#get username, password and target account
username=input("Enter your username:")
password=input("Enter your password:")
target_account=input("Enter the target account username:")

#type in the username and password, click the login button
username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")
username_input.send_keys(username)
password_input.send_keys(password)
login_button = browser.find_element(By.XPATH,"//button[@type='submit']")
login_button.click()
sleep(8)

##GET FOLLOWERS LIST##

#navigate to target account profile webpage
browser.get("https://www.instagram.com/"+target_account+"/")
sleep(3)

#open the follower popup
browser.find_element(By.PARTIAL_LINK_TEXT, "follower").click()
sleep(4)

#scroll to generate all profiles target user follows
scrollable_popup = browser.find_element(By.CLASS_NAME, "_aano")
for i in range(200):
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
    sleep(4)
    
#get and print number of followers 
xpath_followers = "//span[contains(@class, '_aacl _aaco _aacw _aacx _aad7 _aade')]"
followers_elem = browser.find_elements(By.XPATH, xpath_followers)
print(len(followers_elem))
print([e.text for e in followers_elem])
followers_list = [e.text for e in followers_elem]

##GET FOLLOWING LIST##

#navigate back to profile page to close pop-up
browser.get("https://www.instagram.com/"+target_account+"/")
sleep(3)

#open following pop-up
browser.find_element(By.PARTIAL_LINK_TEXT, "following").click()
sleep(4)

#scroll to generate all profiles following target user
scrollable_popup = browser.find_element(By.CLASS_NAME, "_aano")
for i in range(200):
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
    sleep(4)
    
#get and print number of following users
xpath_following = "//span[contains(@class, '_aacl _aaco _aacw _aacx _aad7 _aade')]"
following_elem = browser.find_elements(By.XPATH, xpath_following)
print(len(following_elem))
print([e.text for e in following_elem])
following_list = [e.text for e in following_elem]

#compare the lists to generate a list of 'fake' accounts
not_fake_count = 0
fake_list = []
for profile in following_list:
    if profile in followers_list:
        not_fake_count+=1
    else: 
        fake_list.append(profile)
print("here is the list of people who are 'fake': ", fake_list)

browser.close()
