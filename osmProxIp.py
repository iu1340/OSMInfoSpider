# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
import re
import urllib
import json
import math
import random
from urllib import parse
from test.test_urllib import urlopen
import telnetlib


class OsmProxy:
    # get proxy
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        self._user_agent = user_agent

    def getHTMLText(self, url, proxies):
        try:
            r = requests.get(url, proxies=proxies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except:
            return 0
        else:
            return r.text

    def get_ip_list(self, url):
        headers = {"User-Agent": self.user_agent}
        web_data = requests.get(url,headers)
        print(web_data)
        soup = BeautifulSoup(web_data.text, "lxml")
        ips = soup.find_all('tr')
        ip_list = []
        length = len(ips)
        if length>50:
            length = 50
        for i in range(1, length):
            ip_info = ips[i]
            tds = ip_info.find_all('td')            
            ip_list.append(tds[0].text + ':' + tds[1].text)
        # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
        for ip in ip_list:
            try:
                proxy_temp = {'http': 'http://' + ip,'https': 'http://' + ip}
                requests.get('http://www.njnu.edu.cn/', proxies=proxy_temp)#新的 urllib中没有proxies只能用test的
                # ip_prot = ip.split(":")
                # telnetlib.Telnet(ip_prot[0], port=ip_prot[1], timeout=30)
            except Exception as e:
                ip_list.remove(ip)
                print(e)
            continue
        return ip_list

    def get_random_proxies(self,ip_list):
        # proxy_list = []
        ip =  random.choice(ip_list)
        # for ip in ip_list:
        #     proxy_list.append('http://' + ip)
        # proxy_ip = random.choice(proxy_list)
        proxies = {'http': 'http://' + ip,'https': 'http://' + ip}
        return proxies

        
