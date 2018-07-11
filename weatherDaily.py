# -*- coding:UTF-8 -*-
import requests
import random
import socket
import time
import http.client
from bs4 import BeautifulSoup
import csv


def get_content(url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.weather.com.cn',
        'Upgrade-Insecure-Request': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'
    }

    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, header)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def get_data(html):
        final = []
        bs = BeautifulSoup(html, "html.parser")
        body = bs.body
        '''
        print(body)
        '''
        data1 = body.find('div', {'id': '7d'})
        ul1 = data1.find('ul')
        li = ul1.find_all('li')

        for day in li:
            print(day)
            #python2中，list若包含中文，整体输出时是以十六进制输出的；
            temp = []
            date = day.find('h1').string
            temp.append(date)
            print(temp)
            inf = day.find_all('p')
            temp.append(inf[0].string)

            if inf[1].find('span') is None:
                temperature_highest = None
            else:
                temperature_highest = inf[1].find('span').string
                '''
                temperature_highest = temperature_highest.replace('℃', '')
                '''
            temperature_lowest = inf[1].find('i').string
            '''
            temperature_lowest = temperature_lowest.replace('℃', '')
            '''
            temp.append(temperature_highest)
            temp.append(temperature_lowest)
            final.append(temp)

        return final

def write_data(data, name):
    print(data)
    file_name = name
    with open(file_name, 'a', newline='', encoding='GB2312') as f:   #a 就是追加的意思
            w = csv.writer(f)
            w.writerow(data)


if __name__ == "__main__":
    url = "http://www.weather.com.cn/weather/101070201.shtml"
    html = get_content(url)
    data = get_data(html)
    write_data(data, '/Users/xxx/Desktop/weather.csv')

