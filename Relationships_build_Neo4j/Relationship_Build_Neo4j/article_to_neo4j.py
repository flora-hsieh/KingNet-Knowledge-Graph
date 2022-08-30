import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import mysql.connector as sql
import pymysql
import jaconv
import re
from tqdm import tqdm

# 設定database 並傳入資料
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT urlid, tags FROM SANDBOX.Flora_urlid_tags;")  # 自己設定資料多少(LIMIT盡量限定在10000以內)


#urlid弄成list
# articlelst = []
# for arti in mycursor:
#     articlelst.append(arti)

# # print(urlidlst)
# # print(len(urlidlst))

diag_art_pair = mycursor.fetchall()

from neo4j import GraphDatabase

transaction_execution_commands = []
    
for diag, arti in diag_art_pair:
    neo4j_create_statement = " MATCH (d:Medical_terms) WHERE d.diagnoseID ="+ str(diag) + " WITH d " \
        + "MERGE (a:Articles{name:" + str(arti) + "})" \
        + " MERGE (a)-[:REL]->(d)"
    transaction_execution_commands.append(neo4j_create_statement)
print('s')
try:
    def execute_transactions(transaction_execution_commands):
        data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth = ("neo4j", "password"))
        session = data_base_connection.session()

        for i in tqdm(transaction_execution_commands, desc="進度"):
            session.run(i)

    execute_transactions(transaction_execution_commands)
except Exception as e:
    print("Error occurred:" + str(e))