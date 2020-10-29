import requests
from bs4 import BeautifulSoup
from sys import argv
import os  ################################
import time

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

end = 0
now = 0
file_art = open("all_article.txt", "w", encoding = "utf-8")
file_pop = open("pop6.txt", "w", encoding = "utf-8")
url = "https://www.ptt.cc/bbs/Beauty/index1992.html"
while end == 0:
    r = requests.get(url)
    content = r.text
    time.sleep(1)
    soup = BeautifulSoup(content, "html.parser")
    groupPage = soup.find_all(class_ = "btn-group btn-group-paging")
    if groupPage:
        pages = groupPage[0].find_all('a')
    else:
        time.sleep(1)
        continue
    nextPage = "https://www.ptt.cc" + pages[2].get("href")
    url = nextPage
    title_list = soup.find_all(class_ = "r-ent")
    for s in title_list:
        block1 = s.find_all('a')
        if block1:
            block2 = s.find_all(class_ = "date")
            date = block2[0].string
            month, day = date.split("/", 1)
            m = int(month)
            d = int(day)
            print("m = " + month)
            print("now = " + str(now))
            if m == 1 and now == 0:
                now = 1
            elif now == 0 and m == 12:
                continue
            elif now == 12 and m == 1:
                end = 1
                break
            elif now != m:
                now = m
            if now != 0 and end == 0:
                line = month + day
                link = block1[0].get("href")
                if block1[0].string != None:
                    if block1[0].string.find("[公告]") == -1:
                        line += ","+ block1[0].string + "," + "https://www.ptt.cc" + link
                    else:
                        continue
                else:
                    mailDecode = block1[0].find("span").get("data-cfemail")
                    line += ","+ block1[0].text[:-17] + cfDecodeEmail(mailDecode) + "," + "https://www.ptt.cc" + link
                file_art.write(line + "\n")
                like = s.find("span")
                if like:
                    if like.string == '爆':
                        file_pop.write(line + "\n")