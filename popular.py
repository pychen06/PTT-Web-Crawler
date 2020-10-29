import requests
from bs4 import BeautifulSoup
from sys import argv
import os
import time


start = argv[1]
end = argv[2]
start_date = int(start)
end_date = int(end)

#start_date = 101
#end_date = 110
num_push = 0
num_boo = 0
counter = 0

file_pop = open("pop5.txt", "r", encoding = "utf-8")
line = file_pop.readline()
split_list = line.split(",")
date = int(split_list[0])
url = split_list[-1]
while date < start_date:
    line = file_pop.readline()
    split_list = line.split(",")
    date = int(split_list[0])
    url = split_list[-1]
while date <= end_date:
    url = url.strip("\n")
    counter += 1
    r = requests.get(url)
    content = r.text
    time.sleep(0.5)
    soup = BeautifulSoup(content, "html.parser")
    mainList = soup.find_all(class_ = "bbs-screen bbs-content")
    refList = mainList[0].find_all("a")
    for ref in refList:
        if ref.string != None:
            if ref.string[-4:] == ".jpg" or ref.string[-5:] == ".jpeg" or ref.string[-4:] == ".png" or ref.string[-4:] == ".gif": 
                print(ref.string)
    
    line = file_pop.readline()
    split_list = line.split(",")
    date = int(split_list[0])
    url = split_list[-1]
print(counter)
file_pop.close()
os.system("pause")