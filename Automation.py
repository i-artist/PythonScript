from selenium import webdriver
import pyautogui
import pymssql
import time
import xlrd
import datetime
import redis
REDIS_STORE = redis.Redis(#######################################)
nowTime=datetime.datetime.now().strftime('%Y-%m-%d')#现在
conn = pymssql.connect(######################################)
cursor = conn.cursor()
cursor.execute("select cursor_url from [SinaWeiboAPI].[dbo].[Record_url] where createtime>'{} 00:00:00'".format(nowTime))
keys = [row[0] for row in cursor.fetchall()]

num = REDIS_STORE.scard("Record_Url")
print(num)



browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")
# #
time.sleep(5)

cookies = [{'value': ',,login.sina.com.cn', 'domain': '.weibo.com', 'path': '/', 'expiry': 1566540817, 'name': 'UOR', 'httpOnly': False, 'secure': False}, {'domain': 'weibo.com', 'path': '/', 'value': 'b02489d329584fca03ad6347fc915997', 'name': 'YF-Ugrow-G0', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': '4769f22b37925785aefc96d734d484ed', 'name': 'login_sid_t', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': 'SSL', 'name': 'cross_origin_proto', 'httpOnly': False, 'secure': False}, {'domain': 'weibo.com', 'path': '/', 'value': '572595c78566a84019ac3c65c1e95574', 'name': 'YF-V5-G0', 'httpOnly': False, 'secure': False}, {'value': '1366*7681', 'domain': 'weibo.com', 'path': '/', 'expiry': 1535039980, 'name': 'wb_view_log', 'httpOnly': False, 'secure': False}, {'value': 'e8781eb7dee3fd7f|undefined', 'domain': 'weibo.com', 'path': '/', 'expiry': 1535004938, 'name': 'WBStorage', 'httpOnly': False, 'secure': False}, {'domain': 'weibo.com', 'path': '/', 'value': '00acf392ca0910c1098d285f7eb74a11', 'name': 'YF-Page-G0', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': 'passport.weibo.com', 'name': '_s_tentry', 'httpOnly': False, 'secure': False}, {'value': '7364852227956.571.1535004340351', 'domain': '.weibo.com', 'path': '/', 'expiry': 1850364340, 'name': 'SINAGLOBAL', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': '7364852227956.571.1535004340351', 'name': 'Apache', 'httpOnly': False, 'secure': False}, {'value': '1535004340364:1:1:1:7364852227956.571.1535004340351:', 'domain': '.weibo.com', 'path': '/', 'expiry': 1566108340, 'name': 'ULV', 'httpOnly': False, 'secure': False}, {'value': '1566540814', 'domain': '.weibo.com', 'path': '/', 'expiry': 1566540814.805855, 'name': 'ALF', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': '1535004815', 'name': 'SSOLoginState', 'httpOnly': False, 'secure': False}, {'domain': '.weibo.com', 'path': '/', 'value': '_2A252eiDfDeRhGedJ71YW9ibKwzuIHXVVDhUXrDV8PUNbmtBeLVGgkW9NVh1CXTYnsUtpbVn8xV9X77fsDPumOXJO', 'name': 'SUB', 'httpOnly': True, 'secure': False}, {'value': '0tK7Zzld1oaQ3M', 'domain': '.weibo.com', 'path': '/', 'expiry': 1566540815.805718, 'name': 'SUHB', 'httpOnly': False, 'secure': False}, {'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFiTcJJ0iupzPRKIWU6nz5L5JpX5KzhUgL.Fo2NShBNSonc1hM2dJLoIEBLxKML1K.LB.-LxK-LBKnL1h2LxK-L1K-LBKBLxK.L1h-L1Kzt', 'domain': '.weibo.com', 'path': '/', 'expiry': 1566540815.805658, 'name': 'SUBP', 'httpOnly': False, 'secure': False}, {'value': '1366*7681', 'domain': 'weibo.com', 'path': '/', 'expiry': 1535039737, 'name': 'wb_view_log_1744768687', 'httpOnly': False, 'secure': False}]
time.sleep(1)

for cookie in cookies:
    browser.add_cookie(cookie)
browser.get("https://weibo.com")
time.sleep(8)


ExcelFile = xlrd.open_workbook(r'test.xlsx')
sheet1 = ExcelFile.sheet_names()[0]
sheet = ExcelFile.sheet_by_name(sheet1)
comment = sheet.col_values(1)
url = sheet.col_values(0)
zipped = zip(url,comment)

for key in zipped:
    print(key[0],key[1])
    browser.get(key[0])
    time.sleep(8)

    try:
        browser.find_element_by_css_selector(".WB_publish .p_input .W_input").send_keys("爱吃又会吃的金先生告诉你一个秘密：饮食界也有圈层。越是顶层，越讲究匹配。纯正美食，搭配#百威金尊#的纯粹麦芽，口感对味，经受得起挑剔的味蕾。")
    except:
        print("禁止评论")

    try:
        browser.find_element_by_css_selector(".WB_publish .ico a:nth-of-type(3)").click()

        time.sleep(2)
        pyautogui.click(x=315,y=382,button='left',duration=1.5)
        time.sleep(3.5)
        pyautogui.click(x=804,y=517,button='left',duration=1.5)
    except:
        print("图片ERROR禁止上传")
    time.sleep(10)
    try:
        browser.find_element_by_css_selector(".p_opt .btn a").click()
        REDIS_STORE.sadd("Record_Url", key[0])
    except:
        print("error")

    time.sleep(30)


