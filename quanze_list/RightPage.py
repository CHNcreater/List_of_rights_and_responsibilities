#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# '''
# ## 定义权责清单类（即第一级别的子页面）
# 具体类的属性在本代码最后给出
# '''


# In[ ]:


from selenium import webdriver
import re
import time


# In[ ]:


import json


# In[ ]:


from util import nextPage


# In[ ]:



class Right:
    
    def __init__(self,url,idx):
        self.page = {}
        self.page['idx'] = idx
        self.page['url'] = url
    
    def get_info(self,text):
        ''' 获得基本信息'''
        pat = '<label>(.*?)</label>.*?<div class="desc-content".*?>(.*?)</div>'
        infos = re.findall(pat,text,re.S)# re.S代表‘.’会匹配包括换行符在内的所有字符
        for info in infos:
            self.page[info[0]] = info[1]
        
    def get_urls(self,browser):
        '''获得办事指南页面的urls'''
        pat = '<a title=".*?" href="(.*?)" target="_blank">'
        urls = []
        while True:
            time.sleep(2)
            text = browser.page_source
            tbody = re.search(r'<tbody>(.*?)</tbody>',text,re.S)
            if tbody == None:
                break
            else:
                tbody = tbody.groups()[0]
            turls = re.findall(pat,tbody,re.S)
            
            for st_url in turls:
                if st_url not in urls and (not st_url.startswith('http')):
                    urls.append(st_url)  ## 解决在线申办 以及 申请材料 这两个链接的问题
            
#             urls.extend(turls[::2])  
#             ''' ***在线申办*** 无效的情况下，表格每一行仅有 ***真正的url*** 和 ****申请材料*** 这两个链接重复
#             因此通过上述手段 去重'''
            flag = nextPage(browser,text)
#             print(flag)
            if flag == 0:
#                 print('break')
                break
        s_urls = []
        for turl in urls:
            turl = turl.replace('#matters-part4','')
            if turl not in s_urls:
                s_urls.append(turl)
        self.page['checklist_urls'] = s_urls
        
    def handle_page(self,browser):
        text = browser.page_source
        self.get_info(text)
        self.get_urls(browser)


# In[ ]:


# test
if __name__ == '__main__':
    turl = 'http://www.gdzwfw.gov.cn/portal/affairs-public-duty-list?region=440300&deptCode='
#     turl = 'http://www.gdzwfw.gov.cn/portal/affairs-public-detail?qzqdCode=00288efa-bc84-4176-993f-8e08da4e56f0&amp;deptCode=MB2C94128'
    browser = webdriver.Firefox(log_path = "webdriver.log")
    browser.get(turl)
    time.sleep(0.5)

    right = Right(turl,0)
    right.handle_page(browser)

#     browser.close()
    
    with open('11.json','w+',encoding = 'utf-8') as fout:
        tmp = json.dumps(dict(right.page.items()),ensure_ascii=False,indent = 4)
        fout.write(tmp+'\n')
        fout.write('----------下一级页面----------')

#     for k,v in right.page.items():
#         print(k,v)
    
# '''
# output:
# 行使主体 深圳市规划和自然资源局（深圳市海洋渔业局、深圳市林业局）
# 编码 440217281000
# 类别 行政处罚
# 依据 中华人民共和国渔业港航监督行政处罚规定 中华人...
# 责任事项 
# urls ['/portal/guide/11440300MB2C94128A3440217281000']
# '''


# In[ ]:




