# username.screenshot('1.png')
# backupdatabase = json.loads(open("D:/GIT/temp/database.json", "r").read())
# open("D:/GIT/temp/database_backup.json", "w").write(json.dumps(backupdatabase))


import json
import time 
import os
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def load_env():
    # Check if the script is being run from a file
    if os.path.isfile(__name__):
        # Load .env file from the script's directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
    else:
        # Load .env file from the current directory
        env_path = '.env'
    # Read the .env file
    with open(env_path) as f:
        lines = f.readlines()
    # Parse the lines and set the environment variables
    item = {}
    for line in lines:
        if line.strip():  # Ignore empty lines
            key, value = line.strip().split('=', 1)
            item[key] = value
    return item


def get_credentials(func):
    """
    custom for old.reddit.com login
    """
    vars = func()
    # Get the username and password
    username = vars.get('webusername')
    password = vars.get('webpassword')
    return username, password



def login(INPUT_username,INPUT_password):
    element = browser.find_element(By.ID, 'login_login-main')
    username = element.find_element(By.NAME, 'user')
    username.clear()
    username.send_keys(INPUT_username)
    passwd = element.find_element(By.NAME, 'passwd')
    passwd.clear()
    passwd.send_keys(INPUT_password)
    loginbutton = element.find_element(By.XPATH, '/html/body/div[2]/div[2]/form/div[4]/button')
    loginbutton.submit()




def openitem(item):
    element = browser.find_element(By.XPATH, item)
    element.click()

# item constants 
PROFILEPAGE = "/html/body/div[1]/div[3]/span[1]/a"
COMMENTSPAGE = "/html/body/div[1]/div[2]/ul/li[2]/a"
SUBMITTEDPAGE = "/html/body/div[1]/div[2]/ul/li[3]/a"
UPVOTEDPAGE = "/html/body/div[1]/div[2]/ul/li[4]/a"
DOWNVOTEDPAGE = "/html/body/div[1]/div[2]/ul/li[5]/a"
SAVEDPAGE = "/html/body/div[1]/div[2]/ul/li[7]/a"

def get_entry():
    print("breakpoint 1")
    entry = {}
    dd = browser.find_element(By.CLASS_NAME, 'thing')
    entry["url"] = dd.find_element(By.CLASS_NAME, 'title').get_attribute('href')
    entry["title"] = dd.find_element(By.CLASS_NAME, 'title').text
    entry["myComment"] = dd.find_element(By.CLASS_NAME, 'usertext-body').text
    contextbutton = dd.find_elements(By.CLASS_NAME, 'bylink')[1]
    contextbutton.send_keys(Keys.CONTROL + Keys.RETURN)
    browser.switch_to.window(browser.window_handles[-1])
    print("breakpoint 2")
    time.sleep(1)
    de = browser.find_element(By.CLASS_NAME, 'nestedlisting')
    entry["context"] = de.text.replace(
        '\n\n\n\n\n\n\n\n\n\n\n', "" ).replace(
        'permalinksaveeditdisable inbox repliesdelete', '').replace(
        'permalinkembedsaveeditdisable inbox repliesdeletereply', '').replace(
        'thoughtpermalinkembedsaveparenteditdisable inbox repliesdeletereply', '').replace(
        '[–]','---[-]').split('---')[1:]
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    print("breakpoint 3")
    postbutton = dd.find_element(By.CLASS_NAME, 'title')
    postbutton.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(1)
    print("breakpoint 4")
    try:
        aa = browser.find_element(By.CLASS_NAME, 'expando')
        entry["post"] = aa.find_element(By.CLASS_NAME, 'md').text
    except Exception as e:
        # print(e)
        entry["post"] = "not text"
    browser.close()
    print("breakpoint 5")
    browser.switch_to.window(browser.window_handles[0])
    deletebutton = dd.find_element(By.CLASS_NAME, 'del-button')
    deletebutton.click()
    time.sleep(1)
    # temp_database.append(entry)
    print("breakpoint 6")
    deletebuttonconfirm = dd.find_elements(By.CLASS_NAME, 'yes')[1]
    deletebuttonconfirm.click()
    openitem(COMMENTSPAGE)
    return entry






def init_FF():
    options = webdriver.FirefoxOptions()
    options.headless = False
    browser = webdriver.Firefox(options=options)
    browser.get('https://old.reddit.com')
    time.sleep(5)
    login(*get_credentials(load_env))
    time.sleep(5)
    openitem(PROFILEPAGE)
    openitem(COMMENTSPAGE)
    return browser


# openitem(PROFILEPAGE)
# openitem(COMMENTSPAGE)
# openitem(SUBMITTEDPAGE)
# openitem(UPVOTEDPAGE)
# openitem(DOWNVOTEDPAGE)
# openitem(SAVEDPAGE)


# ----

browser = init_FF()
database= json.loads(open("D:/GIT/temp/database.json", "r").read())
temp_database = json.loads(open("D:/GIT/temp/database.json", "r").read())

len(json.loads(open("D:/GIT/temp/database.json", "r").read()))
len(temp_database)


blank = [print(i["myComment"]) for i in temp_database]



def main():
    get_comments()
    get_submitted()
    get_upvoted()
    get_downvoted()

    get_entry()


get_comments()
def get_comments():
    for i in range(0, 24):
        openitem(COMMENTSPAGE)
        print("loop number: ", i)
        item = get_entry()
        temp_database.append(item)
        openitem(COMMENTSPAGE)
        time.sleep(1)


for i in range(0,4):
    print("loop number: ", i)
    item = None
    item = main()
    # backup cache
    open("d:/git/temp/tempfile.tmp", "a").write(","+json.dumps(item))
    temp_database.append(item)





# write to file
open("D:/GIT/temp/database.json", "w").write(json.dumps(temp_database))


# cache
len(open("d:/git/temp/tempfile.tmp", "r").read().split("url"))



