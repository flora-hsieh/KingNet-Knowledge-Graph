import requests
from urllib.parse import unquote
import json
import urllib.parse


#　抓取單辭字典
url = 'https://www.kingnet.com.tw/ajax/selectDiagnoseList?selectType=list&keyword=&dataIndex=00&dataCnt=8748'
res = requests.get(url)
# r = unquote(res.text)
dls = json.loads(res.text, strict=False)['diagnoseList']
i = 0

for dl in dls:
    dl['englishName'] = urllib.parse.unquote(dl['englishName'])
    dl['name'] = urllib.parse.unquote(dl['name'])
    dl['ID_kingListName'] = i + 1
    i += 1
    


# 抓取各單辭下的相關新聞標題

# for i in range(len(dl)):
#     response = requests.get(f"https://www.kingnet.com.tw/ajax/selectListNews?tag=&keyword={dl[i]['name']}&dateType=&dataIndex=0&dataCnt=10")

# result = []
# activities = response.json()["news"]

# print(activities)

# for activity in activities:
#     title = urllib.parse.unquote(activity["newTitle"])

#     result.append(dict(title=title))

# for i in range(len(dls)):
    
#     dl[i][result[i['title']]]

print(dls[0]['clickCnt'])
