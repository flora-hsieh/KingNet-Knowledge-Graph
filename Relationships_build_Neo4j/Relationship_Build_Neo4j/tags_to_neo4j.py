import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import mysql.connector as sql
import pymysql
import jaconv

# 設定database 並傳入資料
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT article_urlid, tag_name FROM SANDBOX.flora_tag WHERE del IS NULL;")  # 自己設定資料多少(LIMIT盡量限定在10000以內)

taglist = []
for tag in mycursor:
    taglist.append(tag)
uni_taglist = []
for tag in taglist:
    uni_taglist.append(jaconv.z2h(tag[1], kana=False, ascii=True, digit=True))

idlst = []
for tag in taglist:
    idlst.append(str(tag[0]))

# zipped = []
# for i in range(len(taglist)):
#     zipped.append(zip(str(taglist[i][0]), uni_taglist[i]))
zipped = zip(idlst, uni_taglist) 


from neo4j import GraphDatabase

transaction_execution_commands = []
    
for z in zipped:
    neo4j_create_statement = "CREATE(:Tags {tag_id:" + str(z[0]) +", name:'" + str(z[1]) +"'})"
    transaction_execution_commands.append(neo4j_create_statement)

try:
    def execute_transactions(transaction_execution_commands):
        data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth = ("neo4j", "password"))
        session = data_base_connection.session()
        for i in transaction_execution_commands:
            session.run(i)

    execute_transactions(transaction_execution_commands)
except Exception as e:
    print("Error occurred:" + str(e))