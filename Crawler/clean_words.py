import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import mysql.connector as sql
import pymysql
import jaconv
import re
import json

# 建立要拔除字的清單
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT tag_name FROM SANDBOX.flora_tag where del IS NULL;")  # 自己設定資料多少(LIMIT盡量限定在10000以內)

not_redundlst = []
for redund in mycursor:
    not_redundlst.append(redund[0])

not_redundset = set(not_redundlst)
# redund_json = json.dumps(redundlst, ensure_ascii=False)
# print(redund_json)
# print(redundlst)

# 找出要對照的字串
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT article_urlid, article_tags FROM SANDBOX.Title_Tags")  # 自己設定資料多少(LIMIT盡量限定在10000以內)

cnt = 0
termdict = dict()
termlst = []

import json

for term in mycursor:
    urlid = term[0]
    try:
        tags = json.loads(term[1])
    except:
        continue

    useful_tags = [
                        {
                            'urlid'     :       urlid,
                            'tags'      :       tag
                        } 
                    for tag in tags if tag in not_redundset]

    termlst += useful_tags

    if useful_tags:
        print(useful_tags[0])

import pickle

with open(r"C:\Users\flora.hsieh\Desktop\Crawler\Content_Tags_Analysis\Result\clean_tag.pkl" ,'wb') as f:
    pickle.dump(termlst, f)

    # for r in not_redundlst:
    #     if r in term[1]:
    #         termdict["urlid"] = term[0]
    #         termdict["tags"] = r
    #         cnt += 1
    #         termdict["total_id"] = cnt
    #         print(termdict)
            
# from distutils.cmd import Command
# import pymysql

# # 資料庫參數設定

# db_settings = {
#     "host": "35.201.178.21",
#     "port": 3306,
#     "user": "sandbox",
#     "password": "aD-Tg.NczW4tAHX9",
#     "db": "SANDBOX",
#     "charset":"utf8"
# }

# try:
#     # 建立Connection物件
#     conn = pymysql.connect(**db_settings)

# except Exception as ex:
#     print(ex)

# # 建立Cursor物件
# with conn.cursor() as cursor:

#     # 新增SQL語法
#     command = "INSERT INTO King_listName(`ID_kingListName`, `diagnoseId`, `englishName`, `name`, `clickCnt`, `shortWord`) VALUES (%s, %s, %s, %s, %s, %s)"
#     # command_1 = "INSERT INTO King_listName(`ID_kingListName`) VALUES (%s)"
#     # 取得另一個file的import


#     charts = King_listName.dls
#     # id = []
#     # for i in range(len(King_listName.dls)):
#     #     id.append(i + 1)
#     for chart in charts:
#         cursor.execute(
#             command, (chart['ID_kingListName'], chart['diagnoseId'], chart['englishName'], chart['name'], chart['clickCnt'], chart['shortWord'])
#         )
#     # for i in id:
#     #     cursor.execute(
#     #         command_1, (i)
#     #     )
# # 儲存變更

# conn.commit()

