from flask import Flask, render_template, request
import undetected_chromedriver.v2 as uchrome

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import json

from imap_tools import MailBox, AND
import traceback

import urllib3

from bs4 import BeautifulSoup as bs

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
webhook_url = 'https://hooks.slack.com/services/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'

driver = None

app = Flask(__name__, template_folder='./templates')

@app.route("/")
def index():
    # open json file and show data
    with open('templates/source.json') as json_file:
        data = json.load(json_file)
        json_file.close()
    return render_template('index.html', dat=data)

@app.route("/saveemail", methods=['GET', 'POST'])
def saveemail():
    # save data
    if request.method=="POST":
        emailMail = request.form.get("txtEmailMail")
        pwdMail = request.form.get("txtPasswordMail")
        emailGoauth = request.form.get("txtEmailGoauth")
        pwdGoauth = request.form.get("txtPasswordGoauth")
        emailSignUp = request.form.get("txtEmailSignUp")
        pwdSignUp = request.form.get("txtPasswordSignUp")
        pwdSignUpV = request.form.get("txtPasswordSignUpV")
        with open('templates/source.json', 'w') as outfile:
            data_tosave = {
                "withemail" : 
                    {
                        "uname" : emailMail,
                        "pwd" : pwdMail
                    },
                "withgoauth" : 
                    {
                        "uname" : emailGoauth,
                        "pwd" : pwdGoauth
                    },
                "signup": 
                    {
                        "uname": emailSignUp, 
                        "ahapwd": pwdSignUp,
                        "apppwd": pwdSignUpV
                    }                    
            }
            json.dump(data_tosave, outfile)
            outfile.close()     
        return render_template('done.html')

def activateChromeLogPass():
    # Chrome in stealth
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = uchrome.Chrome(options=op)
    driver.get('https://app.earnaha.com/sat')
    driver.maximize_window()
    # read login and password
    with open('templates/source.json') as json_file:
        data = json.load(json_file)
        json_file.close()
    return {"drv":driver, "dat":data}

@app.route("/autosigninemail")
def autosigninemail():
    temp = activateChromeLogPass()
    # click Login Button and then input email and password from index.html page
    btnLogin = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[2]')))
    btnLogin.click()
    txtEmail = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    txtEmail.send_keys(temp["dat"]["withemail"]["uname"])
    txtPwd = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    txtPwd.send_keys(temp["dat"]["withemail"]["pwd"])
    btnContinue = temp["drv"].find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[2]/button')
    btnContinue.click()
    sendNofitication("autosignin with email : done")
    return {"result":checkElementIfExist(temp["drv"], "MuiButtonBase-root", 'byclassname')}

@app.route("/autosigninoauth") 
def autosigninoauth():
    temp = activateChromeLogPass()
    # click Login Button 
    btnLogin = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[2]')))
    btnLogin.click()
    # click Continue with Google Button
    btnGoogle = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/section/div/div/div/div[3]/form/button')))
    btnGoogle.click()
    # input email 
    txtEmail = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierId"]')))
    txtEmail.send_keys(temp["dat"]["withgoauth"]["uname"])
    # next button
    btnNext = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button/span')))
    btnNext.click()
    # password
    txtPwd = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    txtPwd.send_keys(temp["dat"]["withgoauth"]["pwd"])
    btnNext2 = temp["drv"].find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
    btnNext2.click()
    sendNofitication("autosignin with google oauth : done")
    return {"res":checkElementIfExist(temp["drv"], "MuiButtonBase-root", 'byclassname')}

@app.route("/autosignoutemail") 
def autosignoutemail():
    temp = activateChromeLogPass()
    # click Login Button and then input email and password from index.html page
    btnLogin = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[2]')))
    btnLogin.click()
    txtEmail = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    txtEmail.send_keys(temp["dat"]["withemail"]["uname"])
    txtPwd = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    txtPwd.send_keys(temp["dat"]["withemail"]["pwd"])
    btnContinue = temp["drv"].find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[2]/button')
    btnContinue.click()
    time.sleep(4)
    # find profile button
    btnProfile = temp["drv"].find_element(By.ID, 'nav-profile')
    btnProfile.click()
    # find setting button
    btnSetting = temp["drv"].find_element(By.CSS_SELECTOR, '[data-testid="menu-setting"]')
    btnSetting.click()
    # find logout button
    btnLogout = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text() = "LOG OUT"]')))
    btnLogout.click()
    # find YES button to logout
    btnYes = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text() = "Yes"]')))
    btnYes.click()
    sendNofitication("autosignout : done")
    return {"res":checkElementIfExist(temp["drv"], '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[2]', 'byxpath')}

@app.route("/autoeditprofile") 
def autoeditprofile():
    temp = activateChromeLogPass()
    # click Login Button and then input email and password from index.html page
    btnLogin = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[2]')))
    btnLogin.click()
    txtEmail = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    txtEmail.send_keys(temp["dat"]["withemail"]["uname"])
    txtPwd = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    txtPwd.send_keys(temp["dat"]["withemail"]["pwd"])
    btnContinue = temp["drv"].find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[2]/button')
    btnContinue.click()
    time.sleep(3)
    # find profile button
    btnProfile = temp["drv"].find_element(By.ID, 'nav-profile')
    btnProfile.click()
    # find myProfile button
    btnProfile = temp["drv"].find_element(By.CSS_SELECTOR, '[data-testid="menu-account"]')
    btnProfile.click()
    # find calender
    inCalender = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.NAME, 'birthday')))
    inCalender.click()
    # find date to change
    btnDate = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/button')))
    btnDate.click()
    time.sleep(2)
    # find YES button to change date
    btnYes = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div[3]/button[2]')))
    btnYes.click()
    sendNofitication("auto edit profile : done")
    return {"res":checkElementIfExist(temp["drv"], '//*[@id="__next"]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/form/div[3]/button[2]', 'byxpath')}

@app.route("/autosignupemail")
def autosignupemail():
    temp = activateChromeLogPass()
    # click Login Button and then input email and password from index.html page
    btnSignUp = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[3]/div[2]/div/button[1]')))
    btnSignUp.click()
    txtEmail = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    txtEmail.send_keys(temp["dat"]["signup"]["uname"])
    txtPwd = WebDriverWait(temp["drv"], 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    txtPwd.send_keys(temp["dat"]["signup"]["ahapwd"])
    btnContinue = temp["drv"].find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[2]/button')
    btnContinue.click()
    time.sleep(5)
    urlVer = ''
    # email check to verfify
    with MailBox(SMTP_SERVER).login(temp["dat"]["signup"]["uname"], temp["dat"]["signup"]["apppwd"]) as mailbox:
        for msg in mailbox.fetch(AND(from_='earnaha.com')):
            if msg.from_=="service@earnaha.com" and msg.subject=="Please verify your email":
                print(msg.from_)
                tmp = bs(msg.html, features = "html.parser")
                cont = tmp.find_all('a')
                urlVer = cont[1].contents[0]

    # Verification Process
    driver2 = uchrome.Chrome()
    driver2.get(urlVer)
    driver2.maximize_window()
    return {"result":checkElementIfExist(temp["drv"], "MuiButtonBase-root", 'byclassname')}

def sendNofitication(msg):
    # send to slack
    try:
        slack_message = {'text': msg}
        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body = json.dumps(slack_message),
                                headers = {'Content-Type': 'application/json'},
                                retries = False)
    except:
        traceback.print_exc()

def checkElementIfExist(driver, locator, type):
    if type=='byclassname':
        try:
            driver.find_element(By.CLASS_NAME, locator)
            return True
        except NoSuchElementException:
            return False
    else:
        try:
            driver.find_element(By.XPATH, locator)
            return True
        except NoSuchElementException:
            return False


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

