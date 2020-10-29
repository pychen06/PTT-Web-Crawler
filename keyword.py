import requests
from bs4 import BeautifulSoup
import time

start_date = 901
end_date = 902
keyword = "2017"
num_push = 0
num_boo = 0
counter = 0

file_all = open("all_articles.txt", "r", encoding = "utf-8")
line = file_all.readline()
split_list = line.split(",")
date = int(split_list[0])
url = split_list[-1]
while date < start_date:
    line = file_all.readline()
    split_list = line.split(",")
    date = int(split_list[0])
    url = split_list[-1]
while date <= end_date:
    print(split_list[1])
    url = url.strip("\n")
    counter += 1
    r = requests.get(url)
    content = r.text
    time.sleep(0.5)
    soup = BeautifulSoup(content, "html.parser")
    mainList = soup.find_all(class_ = "bbs-screen bbs-content")
    cutIndex = mainList[0].text.index("※ 發信站")
    cutContent = mainList[0].text[:cutIndex]
    if keyword in cutContent:
        refList = mainList[0].find_all("a")
        for ref in refList:
            if ref.string != None:
                if ref.string[-4:] == ".jpg" or ref.string[-5:] == ".jpeg" or ref.string[-4:] == ".png" or ref.string[-4:] == ".gif": 
                    print(ref.string)
    
    line = file_all.readline()
    split_list = line.split(",")
    date = int(split_list[0])
    url = split_list[-1]
file_all.close()