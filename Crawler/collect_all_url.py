import requests
from urllib.parse import unquote
import json
import urllib.parse
import time
import random
from distutils.cmd import Command
import pymysql
from tqdm import tqdm 

# 寫一個function上傳mysql

def URL_to_mysql(input):
    db_settings = {
    "host": "35.201.178.21",
    "port": 3306,
    "user": "sandbox",
    "password": "aD-Tg.NczW4tAHX9",
    "db": "SANDBOX",
    "charset":"utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

    except Exception as ex:
        print(ex)

    # 建立Cursor物件
    with conn.cursor() as cursor:

        # 新增SQL語法
        command = "INSERT INTO Urls_page(`idurls_page`,`diagnoseId`,`titleURL`) VALUES (%s, %s, %s)"
        # command_1 = "INSERT INTO King_listName(`ID_kingListName`) VALUES (%s)"
        
        
        cursor.execute( 
            command , ( input['idurls_page'], input['diagnoseId'], input['titleUrl']
                )
                )
    
    # 儲存變更

    conn.commit()
def error_to_mysql(input):
    db_settings = {
    "host": "35.201.178.21",
    "port": 3306,
    "user": "sandbox",
    "password": "aD-Tg.NczW4tAHX9",
    "db": "SANDBOX",
    "charset":"utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

    except Exception as ex:
        print(ex)

    # 建立Cursor物件
    with conn.cursor() as cursor:

        # 新增SQL語法
        command = "INSERT INTO Urls_page(`idurls_page`,`diagnoseId`,`titleURL`) VALUES (%s, %s, %s)"
        
        
        cursor.execute( 
            command , ( input['idurls_page'], input['diagnoseId'], input['titleUrl']
                )
                )
        # for i in id:
        #     cursor.execute(
        #         command_1, (i)
        #     )
    # 儲存變更

    conn.commit()


# complete


def name_to_mysql(input):
    db_settings = {
    "host": "35.201.178.21",
    "port": 3306,
    "user": "sandbox",
    "password": "aD-Tg.NczW4tAHX9",
    "db": "SANDBOX",
    "charset":"utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

    except Exception as ex:
        print(ex)

    # 建立Cursor物件
    with conn.cursor() as cursor:

        # 新增SQL語法
        command = "INSERT INTO TEST_title(`titleName`) VALUES (%s)"
       
        
        cursor.execute( 
            command, ( input
            )
            )
        # for i in id:
        #     cursor.execute(
        #         command_1, (i)
        #     )
    # 儲存變更

    conn.commit()










#　抓取單辭字典
u = 'https://www.kingnet.com.tw/ajax/selectDiagnoseList?selectType=list&keyword=&dataIndex=00&dataCnt=8748'
res = requests.get(u)
headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
# r = unquote(res.text)
dls = json.loads(res.text)['diagnoseList']

# print(len(dls))

# 抓取各單辭典下方的所有相關新聞title清單的頁數
def page_cnt(n):
    a = n
    b = 0

    yield b

    while b < (a//10)*10:
        yield b + ((a//10)*10)//(a//10)
        b = b + ((a//10)*10)//(a//10) 

URL = []

i = 1
url = dict()
for dl in tqdm(dls, desc="URLlist"):    
    try:
        # 那個詞下總共有多少文章
        total = (requests.get(f"https://www.kingnet.com.tw/ajax/selectListNews?tag=&keyword={dl['name']}&dateType=&dataIndex=0&dataCnt=60")).json()["total"]
        # print(total)

        
        for p in page_cnt(total):    
            url['idurls_page'] = i
            url['diagnoseId'] = dl['diagnoseId'] 
            url['titleUrl'] = "https://www.kingnet.com.tw/ajax/selectListNews?tag=&keyword=%s&dateType=&dataIndex=%s&dataCnt=10" % (dl['name'], p)
            URL_to_mysql(url)

        time.sleep(random.uniform(1,2))
    
    except Exception as e:
        print("Error occurred:" + str(e))
        url['idurls_page'] = i
        url['diagnoseId'] = dl['diagnoseId']
        url['titleUrl'] = str(e)
        error_to_mysql(url)
        i += 1


