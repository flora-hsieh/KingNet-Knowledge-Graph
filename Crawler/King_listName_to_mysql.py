from distutils.cmd import Command
import pymysql
import King_listName

# 資料庫參數設定

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
    command = "INSERT INTO King_listName(`ID_kingListName`, `diagnoseId`, `englishName`, `name`, `clickCnt`, `shortWord`) VALUES (%s, %s, %s, %s, %s, %s)"
    # command_1 = "INSERT INTO King_listName(`ID_kingListName`) VALUES (%s)"
    # 取得另一個file的import


    charts = King_listName.dls
    # id = []
    # for i in range(len(King_listName.dls)):
    #     id.append(i + 1)
    for chart in charts:
        cursor.execute(
            command, (chart['ID_kingListName'], chart['diagnoseId'], chart['englishName'], chart['name'], chart['clickCnt'], chart['shortWord'])
        )
    # for i in id:
    #     cursor.execute(
    #         command_1, (i)
    #     )
# 儲存變更

conn.commit()


