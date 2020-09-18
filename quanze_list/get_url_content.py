#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: yinbo.qiao
# File: get_url_content.py
# datetime: 2020/8/31 10:48
# software: PyCharm

import requests
import time
import re
from selenium import webdriver
from quanze_list.util import *

path1 = 'sfdrive\geckodriver.exe'
# hurl = 'http://www.guizhou.gov.cn/zwfw/'
# browser = webdriver.Firefox(executable_path = path1)
# browser.get(url)
# time.sleep(10)
# text = browser.page_source


# html = requests.get(
#     'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_index&istest=1&areacode=520100')
# html.encoding = 'utf-8'
# text = html.text
# pat = '<div class="layui-col-xs3 lch_list-item bmfont"(.*?)>(.*?)</div>'
# department_info = re.findall(pat, text)
# # print(len(department_info))  51个
prefix = 'http://zwfw.guizhou.gov.cn/'
# url_list = []
# for item in department_info:
#     url = re.match(r' mburl="(.*?)" ', item[0]).group(1)
#     if url:
#         if url[0:27] == 'http://zwfw.guizhou.gov.cn/':
#             mburl = url[27:]
#         else:
#             mburl = url
#         areacode = 'areacode=520000'
#     else:
#         mburl = '/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_bmqjd&istest=1'
#         areacode = 'areacode=520000&areacode=520000'
#     ocode = 'ocode=' + re.search(r'ocode="(.*?)" ', item[0]).group(1)
#     orgcode = 'orgcode=' + re.search(r'orgcode="(.*?)"', item[0]).group(1)
#     url_list.append(prefix + mburl + '&' + ocode + '&' + orgcode + '&' + areacode)
#
#
# def check_reachable(url_list):
#     count = 0
#     for item in url_list:
#         r = requests.get(item, timeout=5)
#         code = r.status_code
#         if code == 200:
#             count += 1
#         else:
#             print("存在不可达网站，该网站网址为：" + item)
#     if count == len(url_list):
#         print("全部网址都可达！")


# level2_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_bmqjd&istest=1&ocode=-4188128443937240449&orgcode=35070&areacode=520000'
# region_code = '520000'
#
#
# path1 = 'D:\anaconda3\envs\pytorch\Scripts\phantomjs.exe'
# browser = webdriver.Firefox(executable_path=path1)
# browser = webdriver.PhantomJS()
# browser.get(level2_url)
# time.sleep(5)
# level2_text = browser.page_source
#
# def get_url_list(text):
#     level2_pat = '<button class="layui-btn" onclick="openlink\(\'/eptemp.aspx\?t=Znzw.bgt_Html.bgt_ty.bgt_bszn.*?>'
#     guide_info = re.findall(level2_pat, text)
#     guide_info = [item.replace('amp;', '') for item in guide_info if item.find('+') < 0]
#     level3_url = [prefix + item[45:-4] + '&areacode=520000' for item in guide_info]
#     return level3_url
# while True:
#     # # with open('level2_page.txt','w+',encoding='utf-8') as fout:
#     # #     fout.write(level2_text)
#     #
#     # 提取办事指南的link
#     level3_url = get_url_list(level2_text)
#     if len(level3_url)==0:
#         browser.refresh()
#         level3_url = get_url_list(level2_text)
#     else:
#         print(level3_url)
#         print(len(level3_url))
#
#     flag = nextPage(browser, level2_text)
#     if flag == 1:
#         level2_text = browser.page_source
#     else:
#         break
#
# from quanze_list.util import is_reachable
# print(is_reachable(level3_url))

# with open('sourcepage.txt','w+',encoding='utf-8') as fout:
#     fout.write(text)
from bs4 import BeautifulSoup

level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=20140826105015016582&orgcode=-4188128443937240449&areacode=520000'
level3_html = requests.get(level3_url)
level3_html.encoding = 'utf-8'
level3_text = level3_html.text
pat = '<table class="bszn-table layui-table" style="table-layout: fixed;">.*?事项名称.*?</table>'
result = re.search(pat, level3_text, re.S)
result = result.group()
sub_pat = re.compile('<!--(.*?)-->', re.S)
private_pat = re.compile('<tr class="tongban2" style="display:none;">(.*?)</tr>', re.S)
head_pat = '<td class="td-title">(.*?)</td>'
body_pat = '<td.*?>(.*?)</td>'
result_0 = re.sub(sub_pat, '', result)
result_1 = re.sub(private_pat, '', result_0)
head = re.findall(head_pat, result_1, re.S)
print(head)
print(len(head))
result_2 = re.sub(head_pat, '', result_1)
print(result_2)
body = re.findall(body_pat, result_2, re.S)
body = [item.strip() for item in body if item.find('在线申请') < 0
        and item.find('政府服务热线') < 0
        and item.find('是否收费') < 0]
print(body)
print(len(body))

# basic_infos_pat = '<table class="bszn-table layui-table" style="table-layout: fixed;">.*?</table>'
# basic_infos = re.search(basic_infos_pat,level3_text,re.S)
# basic_infos_soup = BeautifulSoup(basic_infos.group(0),'html.parser')
# print(basic_infos_soup.find_all('td'))

# with open('level3_website.txt', 'w+', encoding='utf-8') as fout:
#     fout.write(level3_text)
