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


# item constants 
PROFILEPAGE = "/html/body/div[1]/div[3]/span[1]/a"
COMMENTSPAGE = "/html/body/div[1]/div[2]/ul/li[2]/a"
SUBMITTEDPAGE = "/html/body/div[1]/div[2]/ul/li[3]/a"
UPVOTEDPAGE = "/html/body/div[1]/div[2]/ul/li[4]/a"
DOWNVOTEDPAGE = "/html/body/div[1]/div[2]/ul/li[5]/a"
SAVEDPAGE = "/html/body/div[1]/div[2]/ul/li[7]/a"


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



def login(browser, INPUT_username,INPUT_password):
    element = browser.find_element(By.ID, 'login_login-main')
    username = element.find_element(By.NAME, 'user')
    username.clear()
    username.send_keys(INPUT_username)
    passwd = element.find_element(By.NAME, 'passwd')
    passwd.clear()
    passwd.send_keys(INPUT_password)
    loginbutton = element.find_element(By.XPATH, '/html/body/div[2]/div[2]/form/div[4]/button')
    loginbutton.submit()




def openitem(browser, item):
    element = browser.find_element(By.XPATH, item)
    element.click()


def get_context(browser, browserInstance):
    contextbutton = browserInstance.find_elements(By.CLASS_NAME, 'bylink')[1]
    contextbutton.send_keys(Keys.CONTROL + Keys.RETURN)
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(1)
    de = browser.find_element(By.CLASS_NAME, 'nestedlisting')
    output = de.text.replace(
        '\n\n\n\n\n\n\n\n\n\n\n', "").replace(
        'permalinksaveeditdisable inbox repliesdelete', '').replace(
        'permalinkembedsaveeditdisable inbox repliesdeletereply', '').replace(
        'thoughtpermalinkembedsaveparenteditdisable inbox repliesdeletereply', '').replace(
        '[–]','---[-]').split('---')[1:]
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    return output
    

def delete_item(browser, browserInstance):
    try:
        deletebutton = browserInstance.find_element(By.CLASS_NAME, 'del-button')
        deletebutton.click()
        time.sleep(1)
        deletebuttonconfirm = browserInstance.find_elements(By.CLASS_NAME, 'yes')[1]
        deletebuttonconfirm.click()
        return True
    except Exception as e:
        print(e)
        return False
    


def get_post(browser, browserInstance):
    postbutton = browserInstance.find_element(By.CLASS_NAME, 'title')
    postbutton.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(1)
    try:
        aa = browser.find_element(By.CLASS_NAME, 'expando')
        text = aa.find_element(By.CLASS_NAME, 'md').text
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return text
    except Exception as e:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return "not text"


for count, browserInstance in enumerate(browser.find_elements(By.CLASS_NAME, 'thing')):
    count, get_post(browser, browserInstance)


# entry["deleted"] = delete_item(browser, browserInstance)
def get_comments(browser):
    pageitems = []
    for count, browserInstance in enumerate(browser.find_elements(By.CLASS_NAME, 'thing')):
        print(count)
        entry = {}
        entry["url"] = browserInstance.find_element(By.CLASS_NAME, 'title').get_attribute('href')
        entry["title"] = browserInstance.find_element(By.CLASS_NAME, 'title').text
        entry["myComment"] = browserInstance.find_element(By.CLASS_NAME, 'usertext-body').text
        entry["context"] = get_context(browser,browserInstance)
        entry["post"] = get_post(browser, browserInstance)
        pageitems.append(entry)
    return pageitems




def init_FF():
    options = webdriver.FirefoxOptions()
    options.headless = False
    browser = webdriver.Firefox(options=options)
    browser.get('https://old.reddit.com')
    time.sleep(5)
    return browser


def init_profilePage(browser):
    login(browser, *get_credentials(load_env))
    time.sleep(5)
    openitem(browser, PROFILEPAGE)
    openitem(browser, COMMENTSPAGE)





# ----
temp_database = json.loads(open("D:/GIT/temp/database.json", "r").read())

len(json.loads(open("D:/GIT/temp/database.json", "r").read()))
len(temp_database)


blank = [print(i["myComment"]) for i in temp_database]



def main(browser):
    ddd = get_comments(browser)
    for d in ddd:
        temp_database.append(d)
        open("d:/git/temp/tempfile.tmp", "a").write(","+json.dumps(d))
    

    # get_comments()
    # get_submitted()
    # get_upvoted()
    # get_downvoted()
    # get_commentItem()


browser = init_FF()
init_profilePage(browser)
main(browser)












# write to file
open("D:/GIT/temp/database.json", "w").write(json.dumps(temp_database))

# cache len
len(open("d:/git/temp/tempfile.tmp", "r").read().split("url"))