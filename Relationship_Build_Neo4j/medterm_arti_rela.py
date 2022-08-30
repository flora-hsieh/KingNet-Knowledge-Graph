import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import mysql.connector as sql
import pymysql
import jaconv
import re

# 設定database 並傳入資料
host = "35.201.178.21" 
user = "sandbox"
password = "aD-Tg.NczW4tAHX9"
database = "SANDBOX"
port = '3306'

my_eng = create_engine('mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + database, echo = False )


mysqldb = mysql.connector.connect(host = "35.201.178.21", user = "sandbox", password = "aD-Tg.NczW4tAHX9", database = "SANDBOX" )
mycursor = mysqldb.cursor()
mycursor.execute("SELECT diagnoseId, englishName, `name`, shortWord FROM SANDBOX.King_listName;")  # 自己設定資料多少(LIMIT盡量限定在10000以內)

from neo4j import GraphDatabase

transaction_execution_commands = []
for my in mycursor:
    neo4j_create_statement = "MATCH(medterm:Medical_terms{diagnoseID:" + str(my[0]) +"}),(article:Articles{diagnoseID:" + str(my[0]) +"}) WHERE medterm.diagnoseID = article.diagnoseID MergeCREATE(article) - [:articles_related_to_the_term] -> (medterm)"
    transaction_execution_commands.append(neo4j_create_statement)

def execute_transactions(transaction_execution_commands):
    data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth = ("neo4j", "password"))
    session = data_base_connection.session()
    for i in transaction_execution_commands:
        session.run(i)

execute_transactions(transaction_execution_commands)

