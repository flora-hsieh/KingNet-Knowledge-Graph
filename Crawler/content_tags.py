import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import requests
import json
from urllib.parse import unquote
import urllib.parse
from distutils.cmd import Command
import pymysql
import pandas as pd
import mysql.connector as sql
from tqdm import tqdm
from bs4 import BeautifulSoup
import re

# 寫一個function上傳mysql

def to_mysql(input):
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
        command = "INSERT INTO SANDBOX.Title_Tags VALUES (%s, %s, %s, %s)"
        # command_1 = "INSERT INTO King_listName(`ID_kingListName`) VALUES (%s)"
        
        
        cursor.execute( 
            command , ( input['article_id'], input['article_urlid'], input['article_content'], input['article_tags']
                )
                )
    
    # 儲存變更

    conn.commit()




# 設定database 並傳入資料
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT DISTINCT articleUrls FROM All_Titles LIMIT 5000 OFFSET 6563;")  # 自己設定資料多少(LIMIT盡量限定在10000以內)

cnt = 6562
tagdict = dict()
for url in tqdm(mycursor, desc='completed'):
    # 爬蟲
    r = requests.get(url[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    # tags
    tags_attr = {"itemprop": "keywords"}
    a_tags = soup.find_all("span", attrs = tags_attr)
    tag_clease = re.compile('#(\D+)')
    
    # urlid
    regex = re.compile('\d+')
    match = regex.search(url[0])

    
    # 內文
    content_attr = {"itemprop": "articleBody"}
    contents = soup.find("div", attrs= content_attr)
    taglist = []
    contentlist = []
    cnt += 1

    
    
    # 包成dictionary
    tagdict['article_id'] = cnt
    tagdict['article_urlid'] = match.group(0)
    try:
        for content in contents:
            contentlist.append(content.get_text())
        content = json.dumps(contentlist, ensure_ascii=False)
        tagdict['article_content'] = unquote(content)
    except:
        content_attr = {"itemprop": "articleBody"}
        contents = soup.find("div", attrs= content_attr)
        for content in contents:
            contentlist.append(content.get_text())
        content = json.dumps(contentlist, ensure_ascii=False)
        tagdict['article_content'] = unquote(content)
    try:    
        for tag in a_tags:
            tag_cleased = tag_clease.search(tag.get_text())
            taglist.append(tag_cleased[1])
            tags = json.dumps(taglist, ensure_ascii=False)
        tagdict['article_tags'] = unquote(tags)
    except Exception as e:
        print(e)
    
    

    to_mysql(tagdict)

