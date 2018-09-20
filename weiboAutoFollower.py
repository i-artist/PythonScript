from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from urllib import parse
import base64
import requests
from io import BytesIO
from PIL import Image
import hashlib
import json
import redis
REDIS_HOST = '123.56.196.177'
REDIS_PORT = 6379
def readAccount():
    file = open("微博账号.txt",'r')
    M_file = file.readlines()
    for AP in M_file:
        ap = AP.replace("\n","")
        a = ap.split("----")[0]
        p = ap.split("----")[-1]
        weiboAutoFollower().Execute(a,p)



class weiboAutoFollower(object):
    def __init__(self):
        self.V_Code_Path = "code.png"
        self.browser = webdriver.Chrome()
        self.browser.get("https://weibo.com/")
        time.sleep(5)
        file = open("微博账号.txt", 'r')
        M_file = file.readlines()
        for AP in M_file:
            ap = AP.replace("\n", "")
            a = ap.split("----")[0]
            p = ap.split("----")[-1]
            self.Execute(a, p)
        # REDIS_STORE = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        # Accounts = REDIS_STORE.hgetall("accounts:weiboPC")
        # for account in Accounts:
        #     try:
        #         print(str(account)[2:-1]+"  "+str(Accounts[account])[2:-1])
        #         self.Execute(str(account)[2:-1],str(Accounts[account])[2:-1])
        #     except Exception as e:
        #         print("挂掉了"+e)
    def Get_Vcode_Number(self,CodePath):
        print("获得验证码")
        appcode = "29a0d6c60f7a46a382307fbfe841d038"
        base64_data = ""
        with open(CodePath, "rb") as f:
            base64_data = base64.b64encode(f.read())
        query_data = {
            "user": "zhong",
            "pass": "",
            "softid": "",
            "codetype": "",
            "file_base64": base64_data
        }
        r = requests.post(
            url="http://upload.chaojiying.net/Upload/Processing.php",
            data=query_data
        )
        result = json.loads(r.text)
        if result["err_no"] == 0:
            return result["pic_str"]

    def Save_Vcode_Image(self):
        print("保存验证码")
        time.sleep(2)
        C_Img = self.browser.find_element_by_css_selector(".login_innerwrap .code img")
        location = C_Img.location
        size = C_Img.size
        print(size, location)
        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha = screenshot.crop((810, 238, 920, 272))
        captcha.save(self.V_Code_Path)

    def Input_Verify_Code(self,code):
        print("输入验证码："+code)
        self.browser.find_element_by_css_selector(".verify .input_wrap .W_input").send_keys(code)

    def LoginClick(self):
        print("点击登录")
        self.browser.find_element_by_css_selector(".login_btn .W_btn_a").click()
    def Execute(self,account,password):
        print("starting")
        self.browser.get("https://weibo.com/")
        time.sleep(5)
        self.browser.find_element_by_css_selector("#loginname").send_keys(account)
        self.browser.find_element_by_css_selector(".password .input_wrap .W_input").send_keys(password)
        time.sleep(3)
        V_Code = self.browser.find_element_by_css_selector(".W_login_form .verify")
        current_url = self.browser.current_url
        if V_Code.is_displayed():
            self.Save_Vcode_Image()
            vcode = self.Get_Vcode_Number(self.V_Code_Path)
            self.Input_Verify_Code(vcode)
            self.LoginClick()
        else:
            self.LoginClick()
        time.sleep(3.5)
        new_url = self.browser.current_url
        if current_url == new_url:
            print("登录失败 A{} P{}".format(account,password))
            return
        else:
            self.browser.get("https://weibo.com/3831522886")
            time.sleep(3)
            self.browser.find_element_by_css_selector(
                ".PCD_header .shadow .opt_box div:nth-of-type(1) a:nth-of-type(1)").click()
            time.sleep(2)
        self.browser.delete_all_cookies()
        print("清除cookie")
weiboAutoFollower()
