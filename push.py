import requests
from bs4 import BeautifulSoup
import time

start_date = 418
end_date = 418
num_push = 0
num_boo = 0
push_dict = {}
boo_dict = {}
start_time = time.time()

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
    r = requests.get(url)
    content = r.text
    time.sleep(0.5)
    soup = BeautifulSoup(content, "html.parser")
    reply_list = soup.find_all(class_ = "push")
    for reply in reply_list:
        tag = reply.find("span").text
        id = reply.find_all("span")[1].text
        if tag == '推 ':
            num_push += 1
            if id in push_dict:
                push_dict[id] += 1
            else:
                push_dict[id] = 1
        elif tag == '噓 ':
            num_boo += 1
            if id in boo_dict:
                boo_dict[id] += 1
            else:
                boo_dict[id] = 1
    print("推: " + str(num_push))
    print("噓: " + str(num_boo))
    
    line = file_all.readline()
    split_list = line.split(",")
    date = int(split_list[0])
    url = split_list[-1]

pushList = sorted(push_dict.items(), key=lambda t: t[1])
booList = sorted(boo_dict.items(), key=lambda s: s[1])
print(pushList[-1])  
print(booList[-1])
end_time = time.time()
print(end_time-start_time)
file_all.close()