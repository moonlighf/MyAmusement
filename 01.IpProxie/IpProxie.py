# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import MySQLdb
import re
import telnetlib
import random
import gzip
import StringIO


def GetHeaders():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"]

    headers = {'User-agent': random.choice(USER_AGENTS),
               'Connection': 'keep - alive',
               'Accept-Encoding': 'gzip, deflate'}
    return headers


def connect_mysql():
    # 数据库配置
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="",
                           db="ipproxie",
                           charset="utf8")
    return conn


def IPspider_xicidaili(cursor, numpage, headers):
    url = 'http://www.xicidaili.com/nn/'
    for num in xrange(1, numpage + 1):
        ipurl = url + str(num)
        request = urllib2.Request(ipurl, headers=headers)
        content = urllib2.urlopen(request).read()
        bs = BeautifulSoup(content, 'html.parser')      # 利用 'html.parser'解析网页
        res = bs.find_all('tr')           # 找到所有tr标签（即<tr>.....</tr>）里面的内容
        for item in res:
            try:
                temp = []
                tds = item.find_all('td')

                Ip_address = tds[1].text.encode('utf-8')
                temp.append(Ip_address)   # 得到  IP

                Ip_port = tds[2].text.encode('utf-8')
                temp.append(Ip_port)   # 得到  端口

                temp.append(tds[5].text.encode('utf-8'))   # 得到  类型  （HTTP/HTTPS）
                vlect = str(tds[6].contents[1])
                time = str(tds[7].contents[1])

                reg = 'title="(.*?)\xe7\xa7\x92">'
                reg_list = re.compile(reg, re.S)
                speed_content = float(re.findall(reg_list, vlect)[0])   # 得到速度
                reg_list = re.compile(reg, re.S)
                time_content = float(re.findall(reg_list, time)[0])       # 得到链接时间
                temp.append(speed_content)
                temp.append(time_content)
                if speed_content > 1 or time_content > 1:
                    continue
                else:
                    try:
                        tn = telnetlib.Telnet(Ip_address, port=Ip_port, timeout=20)
                    except:
                        pass
                    else:
                        sql = "insert into ip values(%s,%s,%s,%s,%s)"
                        n = cursor.execute(sql, temp)
                        conn.commit()
            except IndexError:
                pass


def IPspider_kuaidaili(cursor, numpage, headers):
    url = 'https://www.kuaidaili.com/free/inha/{}/'
    for num in xrange(1, numpage + 1):
        ipurl = url.format(num)
        request = urllib2.Request(ipurl, headers=headers)
        content = urllib2.urlopen(request).read()
        data = StringIO.StringIO(content)
        gzipper = gzip.GzipFile(fileobj=data)
        html = gzipper.read()
        bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        res = bs.find_all('tr')
        for item in res:
            try:
                temp = []
                tds = item.find_all('td')

                Ip_address = tds[0].text.encode('utf-8')
                temp.append(Ip_address)   # 得到  IP
                Ip_port = tds[1].text.encode('utf-8')
                temp.append(Ip_port)   # 得到  端口
                temp.append(tds[3].text.encode('utf-8'))  # 得到  类型
                speed_content = tds[5].text.encode('utf-8')
                speed_content = float(re.findall(r"\d+\.?\d*", speed_content)[0])
                temp.append(speed_content)  # 得到  速度     快代理的这个响应速度和响应时间是一样的。
                temp.append(speed_content)  # 得到  响应时间
                try:
                    tn = telnetlib.Telnet(Ip_address, port=Ip_port, timeout=20)
                except:
                    pass
                else:
                    sql = "insert into ip values(%s,%s,%s,%s,%s)"
                    n = cursor.execute(sql, temp)
                    conn.commit()
            except IndexError:
                pass
                


conn = connect_mysql()
cursor = conn.cursor()
cursor.execute("SELECT * FROM ip")
cds = cursor.fetchall()
for item_Ip in cds:
    Ip_address, Ip_port = item_Ip[0], item_Ip[1]
    try:
        tn = telnetlib.Telnet(str(Ip_address), port=str(Ip_port), timeout=20)
    except:
        cursor.execute("delete from ip where IP=str(Ip_address)")
        conn.commit()
pageNums = 5
headers = GetHeaders()
IPspider_xicidaili(cursor, pageNums, headers)
IPspider_kuaidaili(cursor, pageNums+1, headers)
# 测试表明在execute后，insert 的数据已经进入了mysql,
# 但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
# conn.commit()
cursor.close()
conn.close()
