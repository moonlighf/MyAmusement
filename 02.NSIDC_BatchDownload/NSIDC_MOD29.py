# -*- coding: utf-8 -*-                

import urllib2
import os
from cookielib import CookieJar
from HTMLParser import HTMLParser
import time
import random

def YearMonthDay(x, y):
    BigMonth = [1, 3, 5, 7, 8, 10, 12]
    if y in BigMonth:
        return 31
    elif y ==2:
        if (x % 4 == 0) and (x % 100 != 0) and (x % 400 == 0) :
            return 29
        else:
            return 28
    else:
        return 30


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataList = []
        self.directory = '/'
        self.indexcol = ';'
        self.Counter = 0

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'table':
            self.Counter += 1
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if self.directory in value or self.indexcol in value:
                        break
                    else:
                        self.inLink = True
                        self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == 'table':
            self.Counter +=1

    def handle_data(self, data):
        if self.Counter == 1:
            if self.lasttag == 'a' and self.inLink and data.strip():
                self.dataList.append(data)


# Define function for batch downloading
def BatchJob(Files, cookie_jar):
    with open('D:\\Python_code\\IST_MYD\\error.txt', 'a') as fa:
        for dat in Files:
            if (dat.find("h11v28") != -1 or dat.find("h12v28") != -1) and dat.find("hdf") != -1 and dat.find("xml") == -1:
                print "downloading: ", url + dat
                JobRequest = urllib2.Request(url + dat)
                JobRequest.add_header('cookie', cookie_jar)  # Pass the saved cookie into additional HTTP request
                User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
                JobRequest.add_header('User-Agent', User_Agent)  # Pass the saved cookie into additional HTTP request
                JobRedirect_url = urllib2.urlopen(JobRequest).geturl() + '&app_type=401'

                # Request the resource at the modified redirect url
                maxTryNum =10
                for tries in range(maxTryNum):
                    try:
                        Request = urllib2.Request(JobRedirect_url)
                        Response = urllib2.urlopen(Request)
                        f = open(dat, 'wb')
                        f.write(Response.read())
                        f.close()
                        Response.close()
                        break
                    except:
                        if tries < (maxTryNum - 1):
                            continue
                        else:
                            fa.write("Has tried %d times to access url %s, all failed!", maxTryNum, url + dat)
                            break
            else:
                continue
     

year = 2017
for month in xrange(1, 13):
    # The user credentials that will be used to authenticate access to the data
    username = ""
    password = ""

    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

    cookie_jar = CookieJar()

    opener = urllib2.build_opener(
        urllib2.HTTPBasicAuthHandler(password_manager),
        #urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
        #urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
        urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
    
    dayfinal = YearMonthDay(year, month)
    for x in range(1, dayfinal+1):
        print '****************第' + str(x) + '天*************'
        url = 'https://n5eil01u.ecs.nsidc.org/MOST/MOD29P1N.006/{:04}.{:02}.{:02}/'.format(year, month, x)

        # url = 'https://n5eil01u.ecs.nsidc.org/MOSA/MYD29P1N.006/{:04}.{:02}.{:02}/'.format(year, month, x)
        DirRequest = urllib2.Request(url)
        DirResponse = urllib2.urlopen(DirRequest)

        DirRedirect_url = DirResponse.geturl()
        if x == 1:
            DirRedirect_url += '&app_type=401'

        # Request the resource at the modified redirect url
        DirRequest = urllib2.Request(DirRedirect_url)
        DirBody = urllib2.urlopen(DirRequest).read()

        parser = MyHTMLParser()
        parser.feed(DirBody)
        Files = parser.dataList

        BatchJob(Files, cookie_jar)
        time.sleep(random.randint(5, 20))

