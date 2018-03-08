# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
import requests
import random
import time

username = ''
password = ''
datetime = '这里是我存放时间的 txt 文件，你也可以直接从网站源码里得到哟'

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
]

headers = {'User-agent': random.choice(USER_AGENTS),
           'Connection': 'keep - alive',
           'Accept-Encoding': 'gzip, deflate',
           'Host': 'n5eil01u.ecs.nsidc.org'}


with open(datetime, 'r') as fa:
    for line in fa:
        datanum = line[:-1]
        print '========================= ' + datanum + '==========================='
        url = 'https://n5eil01u.ecs.nsidc.org/GLAS/GLAH12.034/{}/'.format(datanum)
        with requests.Session() as session:
            session.auth = (username, password)
            r1 = session.request('get', url)
            r = session.get(r1.url, auth=(username, password))
            soup = BeautifulSoup(r.content, 'lxml')
            divs = soup.find_all("tr")
            for temp in divs:
                try:
                    filename_h5 = temp.find_all("td")[1].text
                    if ('.H5' in filename_h5) and ('.xml' not in filename_h5):
                        target_url_h5 = url + filename_h5
                        r = session.get(target_url_h5, stream=True, headers=headers)
                        filename = filename_h5[:-3] + '_' + datanum + filename_h5[-3:]
                        with open(filename, 'wb') as f:
                            print 'downloading:    ', target_url_h5
                            for chunk in r.iter_content(100):
                                f.write(chunk)
                        time_sleep = random.randint(1, 10)
                        time.sleep(time_sleep)
                except:
                    pass
