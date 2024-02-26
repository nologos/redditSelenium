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
    global username
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
    try:
        de = browser.find_element(By.CLASS_NAME, 'nestedlisting')
    except Exception as e:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return "no context"
    output = de.text.replace(
        '\n\n\n\n\n\n\n\n\n\n\n',"").replace(
        'permalinkembedsavereport','').replace(
        'permalinksaveparentreportreply','').replace(
        'permalinkembedsaveparentreport','').replace(
        'permalinkembedsaveeditdisable inbox repliesdelete','').replace(
        'permalinksaveeditdisable inbox repliesdelete','').replace(
        'permalinkembedsaveparenteditdisable inbox repliesdelete','').replace(
        'permalinkembedsaveparenteditdisable inbox repliesdeletereply','').replace(
        'permalinkembedsaveparentreportreply','').replace(
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
        localbrowserInstance = deletebutton.find_elements(By.CSS_SELECTOR, '.option.error.active')[0]
        deletebuttonconfirm = localbrowserInstance.find_elements(By.CLASS_NAME, 'yes')[0]
        deletebuttonconfirm.click()
        time.sleep(1)
        return True
    except Exception as e:
        print("error single item delete exception")
        return False
    

def delete_allItems(browser):
    try:
        browserInstances = browser.find_elements(By.CLASS_NAME, 'thing')
        print("found ", len(browserInstances), " items, running delete")
        for browserInstance in browserInstances:
            delete_item(browser, browserInstance)
        browser.refresh()
        return True
    except Exception as e:
        print("error multi delete exception")
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


def get_comments(browser):
    pageitems = []
    openitem(browser, COMMENTSPAGE)
    things = browser.find_elements(By.CLASS_NAME, 'thing')
    for count, browserInstance in enumerate(things):
        print(count, "of " , len(things))
        entry = {}
        entry["url"] = browserInstance.find_element(By.CLASS_NAME, 'title').get_attribute('href')
        entry["title"] = browserInstance.find_element(By.CLASS_NAME, 'title').text
        entry["myComment"] = browserInstance.find_element(By.CLASS_NAME, 'usertext-body').text
        entry["context"] = get_context(browser,browserInstance)
        entry["post"] = get_post(browser, browserInstance)
        pageitems.append(entry)
    openitem(browser, COMMENTSPAGE)
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



def mainpoo(browser, func):
    name = func.__name__
    uname = username 
    try:
        temp_database = json.loads(open(f"D:/GIT/temp/{uname}{name}.json", "r").read())
    except FileNotFoundError as e:
        print("file not found, will create new db")
        temp_database = []
    ddd = func(browser)
    for d in ddd:
        temp_database.append(d)
        open(f"d:/git/temp/{uname}{name}.tmp", "a").write(","+json.dumps(d))
    open(f"D:/GIT/temp/{uname}{name}.json", "w").write(json.dumps(temp_database))
    delete_allItems(browser) # delete switch
    if len(ddd) == 25:
        print("page is full, will run again")
        return True
    else:
        print("page is not full will stop after finish")
        return False


#-------


browser = init_FF()
init_profilePage(browser)

for functions in [get_comments]:
    # get_comments -- download all things from comment tab
    counter = 0
    while mainpoo(browser, functions) and (counter := counter + 1) : 
        print("page ", counter)


