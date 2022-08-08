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



# 設定需要用的containers
SET = dict()
cnt = 577876
idlist = []
diagnoselist = []
titlelist = []
articleUrls = []
All = []


 # 設定database
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT diagnoseId,titleUrl FROM SANDBOX.Urls_page WHERE titleUrl != '''total''' LIMIT 5000 OFFSET 60000;")

# 從爬取的titlelist中取出url並取出文章title
for tuple in tqdm(mycursor, desc="completed"): 
    try: 
        res = requests.get(tuple[1])
        news = json.loads(res.text)['news']  
        for i in range(len(news)):
            cnt += 1
            if cnt % 100 != 0:
                idlist.append(cnt)
                SET["idAll_Titles"] = idlist
                diagnoselist.append(tuple[0])
                SET["diagnoseId"] = diagnoselist
                newTitle = news[i]["newTitle"]
                titlelist.append(unquote(newTitle))
                SET["articleTitles"] = titlelist
                articleUrls.append('https://www.kingnet.com.tw/news/single?newId=' + str(news[i]["newId"]))
                SET["articleUrls"] = articleUrls
                # print(cnt)
                # print(SET)
            else:
                idlist.append(cnt)
                SET["idAll_Titles"] = idlist
                diagnoselist.append(tuple[0])
                SET["diagnoseId"] = diagnoselist
                newTitle = news[i]["newTitle"]
                titlelist.append(unquote(newTitle))
                SET["articleTitles"] = titlelist
                articleUrls.append('https://www.kingnet.com.tw/news/single?newId=' + str(news[i]["newId"]))
                SET["articleUrls"] = articleUrls
                print(cnt)
                df = pd.DataFrame(SET)
                print(df)
                df.to_sql(name= 'All_Titles', con=my_eng, index=False, if_exists='append', chunksize=10000)
                # 清空所有list
                idlist.clear()
                diagnoselist.clear()
                titlelist.clear()
                articleUrls.clear()
        else:
            continue
    except Exception as e:
        print("Error occurred:" + str(e))

# print(SET)
df = pd.DataFrame(SET)
df.to_sql(name= 'All_Titles', con=my_eng, index=False, if_exists='append', chunksize=10000)
# print(df)


