#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import re
import traceback
import time
from bs4 import BeautifulSoup
from quanze_list.util import *
from quanze_list.RightPage import Right
import json
import os
from quanze_list.GuidePage import Guide

path1 = 'sfdrive\geckodriver.exe'

# 贵州省行政区代码
region_code = '''520000 贵州省
520100 贵阳市
520200 六盘水市
520300 遵义市
520400 安顺市
520500 毕节市
520600 铜仁市
522300 黔西南州
522600 黔东南州
522700 黔南州
'''


def run_spider(hurl, datapath, regioncode):
    # 获得url对应的页面信息
    browser = webdriver.Firefox(executable_path=path1)
    browser.get(hurl)
    time.sleep(0.5)
    # 贵州政务服务网站文本
    text = browser.page_source

    browser_rt = webdriver.PhantomJS()  # PhantomJS浏览器驱动，用来提取level2级别，即个机构详细权责清单办事指南的网址
    browser_gd = webdriver.Firefox(executable_path=path1)

    # 网站前缀
    prefix = 'http://zwfw.guizhou.gov.cn'
    default_mburl = '/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_bmqjd&istest=1'

    count = 0
    count1 = 0

    level1_url_info = find_urls(text)  ## 拿到所有行政部门旗舰店网址相关信息
    level1_url_list = fetch_url(level1_url_info, default_mburl, regioncode)  ## 通过处理，得到相关部门旗舰店网址
    # website_check = is_reachable(level1_url_list)  ## 测试是否所有旗舰店网址都可达
    #
    # if website_check == 1:  # 如果网站全部可达，不做任何操作
    #     pass
    # else:
    #     exit(-1)  # 退出程序执行
    # 逐个遍历部门旗舰店
    rt_idx = 0  ### 记录部门编号0-50 共51个部门
    for url in level1_url_list:
        rt_idx += 1
        pid = 0  ### 记录所有代办事项的编号，从0开始，随着部门不同，数量不同
        browser_rt.get(url)
        time.sleep(1)
        level2_html = browser_rt.page_source
        while True:

            # 获取二级地址，也就是各机构的所有办事指南网址
            level2_url_info = find_level2_urls(level2_html)
            level2_url_list = fetch_level2_url(level2_url_info, prefix, regioncode)
            # 如果页面没有加载出来，导致没有获取到页面信息，则刷新页面,重新获取办理指南的链接
            epoch = 0
            while len(level2_url_list) == 0 and epoch < 3:
                browser_rt.refresh()
                level2_html = browser_rt.page_source
                level2_url_info = find_level2_urls(level2_html)
                level2_url_list = fetch_level2_url(level2_url_info, prefix, regioncode)
                epoch += 1

            # 网站可达性检测，200状态码则视为可达网站
            # level2_website_check = is_reachable(level2_url_list)
            # if level2_website_check == 1:  # 如果所有网站可达，不做任何操作
            #     pass
            # else:  # 有网站不可达，跳出循环，并打印出不可访问网站网址
            #     break


            for level2_url in level2_url_list:
                pid += 1
                # 新建文件写入句柄
                with open(datapath + str(rt_idx - 1) + '_' + str(pid - 1) + '.json', 'w+', encoding='utf-8') as fout:
                    browser_gd.get(level2_url)
                    level3_text = browser_gd.page_source  # 包含信息的页面
                    page_guide = Guide(browser_gd, level3_text, level2_url, rt_idx - 1, pid - 1)
                    page_guide.handle_guide()
                    page_guide.disp(fout)

            flag = nextPage(browser_rt, level2_html)  # 查看是否存在下一页
            if flag == 0:  # 不存在下一页则退出当前部门
                break

            time.sleep(2)
            level2_html = browser_rt.page_source  # 刷新页面文本
            count += 1

    browser.close()
    browser_rt.close()
    browser_gd.close()


# 行政区代码
region = region_code.split('\n')

for reg in region[0:2]:
    reg = reg.split(' ')
    datapath = reg[1] + '/'
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    hurl = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_index&istest=1&areacode={}'.format(
        reg[0])
    run_spider(hurl, datapath, reg[0])
