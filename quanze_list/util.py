#!/usr/bin/env python
# coding: utf-8

import re
import time
import requests


def nextPage(browser, text):
    '''
    页面跳转到下一页
    '''
    pat = '<a href="javascript:;" class="layui-laypage-next layui-disabled".*?>下一页</a>'
    if re.search(pat, text) == None:  ### 若当前页不是最后一页，则跳转下一页，并返回标志1，代表页面跳转
        browser.find_element_by_class_name('layui-laypage-next').click()  ## brower变成了下一页
        time.sleep(0.5)
        return 1
    else:  ### 已到达最后一页
        return 0


def replace_text(text):
    text = text.replace('\n', '').replace('\t', '').replace(' ', '')
    return text


def replace_brac(text):
    ''' 去除掉<p...></p> <a ...> 等内容
    而如果其中href = 后面的字符串中包含网址是特定网址
    则保留该网址'''
    result = re.sub(re.compile('<img.*?>',re.S),'',text)
    result = re.sub(re.compile('</?a.*?>',re.S),'',result)
    result = re.sub(re.compile('</?div>',re.S),'',result)
    result = re.sub(re.compile('<span.*?>.*?</span>',re.S),'',result)
    result = re.sub(re.compile('</?p.*?>',re.S),'',result)
    result = re.sub(re.compile('<divstyle.*?>',re.S),'',result)
    result = re.sub(re.compile('<div style.*?>', re.S), '', result)
    return result.replace('\n','').replace('\t','').replace(' ','').replace('&nbsp;','')


def find_urls(text):
    pat = '<div class="layui-col-xs3 lch_list-item bmfont"(.*?)>(.*?)</div>'
    url_list = re.findall(pat, text)
    return url_list


def fetch_url(url_infos, default_mburl, regioncode):
    prefix = 'http://zwfw.guizhou.gov.cn/'
    url_list = []
    for item in url_infos:
        url = re.match(r' mburl="(.*?)" ', item[0]).group(1)
        if url:
            if url[0:27] == 'http://zwfw.guizhou.gov.cn':
                mburl = url[27:]
            else:
                mburl = default_mburl
            areacode = 'areacode=' + regioncode
        else:
            mburl = default_mburl
            areacode = 'areacode=' + regioncode  ###  + '&areacode=' + regioncode
        ocode = 'ocode=' + re.search(r'ocode="(.*?)" ', item[0]).group(1)
        orgcode = 'orgcode=' + re.search(r'orgcode="(.*?)"', item[0]).group(1)
        url_list.append(prefix + mburl + '&' + ocode + '&' + orgcode + '&' + areacode)
    return url_list


# 判断网址列表中的网址是否全部可达
def is_reachable(url_list):
    count = 0
    for item in url_list:
        r = requests.get(item, timeout=5)
        code = r.status_code
        if code == 200:
            count += 1
        else:
            print("存在不可达网站，该网站网址为：" + item)
            return 0
    if count == len(url_list):
        print("全部网址都可达！")
        return 1


def find_level2_urls(level2_text):
    level2_pat = '<button class="layui-btn" onclick="openlink\(\'/eptemp.aspx\?t=Znzw.bgt_Html.bgt_ty.bgt_bszn.*?>'
    guide_info = re.findall(level2_pat, level2_text)
    return guide_info


def fetch_level2_url(level2_url_infos, prefix, regioncode):
    guide_info = [item.replace('amp;', '') for item in level2_url_infos if item.find('+') < 0]
    level3_url = [prefix + item[45:-4] + '&areacode=' + regioncode for item in guide_info]
    return level3_url


def S_search(pat, text):
    t = re.search(pat, text, re.S)
    if t == None:
        text1 = ''
    else:
        text1 = t.groups()[0]
    return text1


def handle_time(v, btm):
    '''
    input: 法定**时限的网页源码
    out: 格式化后的信息  [ 说明，单位，数值 ]
    '''
    rer = ['None', 'None', 'None']
    res = []
    text1 = v
    if 'javascrip' in text1 and 'data-target' in text1:
        patj = 'data-target="(.*?)"'
        idsx = S_search(patj, text1)
        if idsx == "":
            return rer
        else:
            idsx = idsx.replace('#', '')
            text2 = btm.find_all(id=idsx)
            if len(text2) != 0:
                text2 = str(text2[0])
            else:
                text2 = ''
            patbd = '<div class="modal-bd">.*?<p>(.*?)</p>'
            text3 = S_search(patbd, text2)
            res.append(replace_text(text3))
        v = replace_brac(v)
        v = replace_text(v)
        v = re.split('[()]', v)
        if len(v) < 2:
            res.append('无')
            res.append('无')
        else:
            res.append(v[1])
            res.append(v[0])
        return res
    else:
        return rer
