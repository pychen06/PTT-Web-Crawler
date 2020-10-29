import requests
from bs4 import BeautifulSoup
from sys import argv
import time

def compare(s1, s2):
    j = 0
    while j < len(s1) and j < len(s2):
        if ord(s1[j]) < ord(s2[j]):
            return 1
        elif ord(s2[j]) < ord(s1[j]):
            return 0
        j += 1
    if len(s1) < len(s2):
        return 1
    else:
        return 0

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

task = argv[1]
if task == "crawl":
    end = 0
    now = 0
    file_art = open("all_articles.txt", "w", encoding = "utf-8")
    file_pop = open("all_popular.txt", "w", encoding = "utf-8")
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
            time.sleep(0.5)
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
                        if link == "/bbs/Beauty/M.1490936972.A.60D.html":
                            continue
                        elif link == "/bbs/Beauty/M.1494776135.A.50A.html":
                            continue
                        elif link == "/bbs/Beauty/M.1503194519.A.F4C.html":
                            continue
                        elif link == "/bbs/Beauty/M.1504936945.A.313.html":
                            continue
                        elif link == "/bbs/Beauty/M.1505973115.A.732.html":
                            continue
                        elif link == "/bbs/Beauty/M.1507620395.A.27E.html":
                            continue
                        elif link == "/bbs/Beauty/M.1510829546.A.D83.html":
                            continue
                        elif link == "/bbs/Beauty/M.1512141143.A.D31.html":
                            continue
                        if block1[0].string.find("[公告]") == -1:
                            line += ","+ block1[0].string + "," + "https://www.ptt.cc" + link
                        else:
                            if block1[0].string[0] != "[":
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
    file_art.close()
    file_pop.close()
elif task == "push":
    start = argv[2]
    end = argv[3]
    start_date = int(start)
    end_date = int(end)
    filename = "push[" + start + "-" + end + "].txt" 
    num_push = 0
    num_boo = 0
    push_dict = {}
    boo_dict = {}
    
    file_all = open("all_articles.txt", "r", encoding = "utf-8")
    file_push = open(filename, "w", encoding = "utf-8")
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
        url = url.strip("\n")
        r = requests.get(url)
        content = r.text
        time.sleep(0.5)
        soup = BeautifulSoup(content, "html.parser")
        reply_list = soup.find_all(class_ = "push")
        for reply in reply_list:
            if reply.find("span"):
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
        line = file_all.readline()
        split_list = line.split(",")
        if split_list[0] != "":
            date = int(split_list[0])
            url = split_list[-1]
        else:
            break
    
    pushListR = sorted(push_dict.items(), key=lambda t: t[1])
    booListR = sorted(boo_dict.items(), key=lambda s: s[1])
    pushList = list(reversed(pushListR))
    booList = list(reversed(booListR))
    file_push.write("all like: " + str(num_push) + "\n")
    file_push.write("all boo: " + str(num_boo) + "\n")
    sortedPush = []
    sortedBoo = []
    i = 0
    index = 0
    while True:
        if i >= len(pushList):
            break;
        elif i != 0 and pushList[i-1][1] == pushList[i][1]:
            index = 0
            while sortedPush[index][1] != pushList[i][1]:
                index += 1
            while True:
                cmp = compare(sortedPush[index][0], pushList[i][0])
                if cmp == 1:
                    index += 1
                    if index >= len(sortedPush):
                        break
                else:
                    break
            sortedPush.insert(index, pushList[i])
        elif i > 10:
            break
        else:
            index = 0
            sortedPush.append(pushList[i])
        i += 1

    i = 0
    index = 0
    while True:
        if i >= len(booList):
            break;
        elif i != 0 and booList[i-1][1] == booList[i][1]:
            index = 0
            while sortedBoo[index][1] != booList[i][1]:
                index += 1
            while True:
                cmp = compare(sortedBoo[index][0], booList[i][0])
                if cmp == 1:
                    index += 1
                    if index >= len(sortedBoo):
                        break
                else:
                    break
            sortedBoo.insert(index, booList[i])
        elif i > 10:
            break
        else:
            index = 0
            sortedBoo.append(booList[i])
        i += 1
    for i in range(0, 10):
        file_push.write("like #" + str(i+1) + ": " + sortedPush[i][0] + " " + str(sortedPush[i][1]) + "\n")
    for i in range(0, 10):
        file_push.write("boo #" + str(i+1) + ": " + sortedBoo[i][0] + " " + str(sortedBoo[i][1]) + "\n")
    
    file_all.close()
    file_push.close()
elif task == "popular":
    start = argv[2]
    end = argv[3]
    start_date = int(start)
    end_date = int(end)
    filename = "popular[" + start + "-" + end + "].txt" 
    num_push = 0
    num_boo = 0
    counter = 0
    infile = ""
    
    file_pop = open("all_popular.txt", "r", encoding = "utf-8")
    file_popImgur = open(filename, "w", encoding = "utf-8")
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
                    infile += ref.string + "\n"
        
        line = file_pop.readline()
        split_list = line.split(",")
        if split_list[0] != "":
            date = int(split_list[0])
            url = split_list[-1]
        else:
            break
    file_popImgur.write("number of popular articles: " + str(counter) + "\n")
    file_popImgur.write(infile)
    file_pop.close()
    file_popImgur.close()
elif task == "keyword":
    keyword = argv[2]
    start = argv[3]
    end = argv[4]
    start_date = int(start)
    end_date = int(end)
    filename = "keyword(" + keyword + ")[" + start + "-" + end + "].txt" 
    num_push = 0
    num_boo = 0
    counter = 0
    
    file_all = open("all_articles.txt", "r", encoding = "utf-8")
    file_key = open(filename, "w", encoding = "utf-8")
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
                        file_key.write(ref.string + "\n")
        
        line = file_all.readline()
        split_list = line.split(",")
        if split_list[0] != "":
            date = int(split_list[0])
            url = split_list[-1]
        else:
            break
    file_all.close()
    file_key.close()