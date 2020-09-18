#!/usr/bin/env python
# coding: utf-8

# ### Q1  有10项 其中的申请材料部分 部分url有弹窗 无法获取url
# ### Q2 BasicDeal get_filepath 可以改进 如果len(url) == 0

# In[1]:


from selenium import webdriver
import re

import time

from bs4 import BeautifulSoup

from quanze_list.util import *
from quanze_list.RightPage import Right
import requests
import json
import traceback


class BasicPage:
    '''  基类 用于disp/fill函数处理'''

    def __init__(self):
        #         self.f = fout
        self.content = {}

    def fill_content(self, tc1, tc2):
        if len(tc1) == len(tc2):
            for k, v in zip(tc1, tc2):
                if len(v) == 0:
                    continue
                else:
                    self.content[k] = v
            return 1
        else:
            return 0

    def disp(self, fout):
        tmp = json.dumps(self.content, ensure_ascii=False, indent=4)
        fout.write(tmp + '\n')


class BasicInfo(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.head = []
        self.body = []
        pat = '<table class="bszn-table layui-table" style="table-layout: fixed;">.*?事项名称.*?</table>'
        s = re.search(pat, text, re.S)
        if s == None:
            self.text = None
        else:
            s = s.group()
            self.text = s

    def get_infos(self):
        if self.text==None:
            return 0
        else:
            sub_pat = re.compile('<!--.*?-->', re.S)
            private_pat = re.compile('<tr class="tongban2" style="display:none;">.*?</tr>', re.S)
            head_pat = '<td class="td-title".*?>(.*?)</td>'
            head_pat_sub = re.compile('<td class="td-title".*?>(.*?)</td>', re.S)
            head_pat_sub_0 = re.compile('<td rowspan="2" class="td-title">(.*?)</td>', re.S)
            body_pat = '<td.*?>(.*?)</td>'
            result = re.sub(sub_pat, '', self.text)
            result_0 = re.sub(private_pat, '', result)
            service_o = re.findall('service_obectj="(.*?)"', result_0, re.S)
            service_o = service_o[0]
            service_o = service_o.replace('0', '公民').replace('1', '法人').replace('2', '其他组织')
            head = re.findall(head_pat, result_0, re.S)
            self.head = [item.strip() for item in head if item.strip() != '审批收费' and item.strip() != '收费']
            result_1 = re.sub(head_pat_sub, '', result_0)
            result_1 = re.sub(head_pat_sub_0, '', result_1)
            body = re.findall(body_pat, result_1, re.S)
            body = [item.strip() for item in body if item.find('在线申请') < 0 and item.find('在线预约') < 0
                    and item.find('政府服务热线') < 0]

            for k in body:
                k = replace_brac(k)
                if k == '':
                    self.body.append(service_o)
                else:
                    self.body.append(k)

    def handle_infos(self):
        self.get_infos()

        r = self.fill_content(self.head, self.body)
        if r == 0:
            return 0
        else:
            return 1


def handle_evi(v, btm):
    '''
    input: 材料中的详细依据
    out: 格式化后的信息  [ 法规明晨，文号，内容等 ]
    '''
    res = []
    text1 = v
    if 'javascrip' in text1 and 'data-target' in text1:
        patj = 'data-target="(.*?)"'
        idsx = S_search(patj, text1)
        if idsx == "":
            return ""
        else:

            idsx = idsx.replace('#', '')
            text2 = btm.find_all(id=idsx)

            if len(text2) != 0:
                text2 = str(text2[0])
            else:
                text2 = ''
            #             print(text2)
            patbd = r'<table.*?>(.*?)</table>'
            #             patbd = '<div class="modal-bd">.*?<p>(.*?)</p>' ###############################################################毁在这个<p></p>
            text3 = S_search(patbd, text2)

            ths = re.findall('<th>(.*?)</th>', text3, re.S)
            tds = re.findall('<td>(.*?)</td>', text3, re.S)

            edict = {}
            for k, v in zip(ths, tds):
                k = replace_brac(k)
                k = replace_text(k)
                v = replace_brac(v)
                v = replace_text(v)
                edict[k] = v
            #             print(edict)
            return str(edict)

    else:
        return ''


def handle_req(v, btm):
    '''
    input: 材料中的其他要求
    out: 格式化后的信息  [ 法规明晨，文号，内容等 ]
    '''
    res = {}
    text1 = v
    if 'javascrip' in text1 and 'data-target' in text1:
        patj = 'data-target="(.*?)"'
        idsx = S_search(patj, text1)
        if idsx == "":
            return ""
        else:

            idsx = idsx.replace('#', '')
            text2 = btm.find_all(id=idsx)

            if len(text2) != 0:
                text2 = str(text2[0])
            else:
                text2 = ''
            #             print(text2)
            #             patbd = r'<table.*?>(.*?)</table>'
            patbd = '<div class="modal-bd">.*?<p>(.*?)</p>'
            text3 = S_search(patbd, text2)
            text3 = text3.replace('\n', '').replace('\t', '')
            tlst = text3.split('<br/>')
            if len(tlst) == 1:
                return text3
            else:
                for tt in tlst[:-1]:
                    tt = tt.split('：')
                    if len(tt) < 2:
                        res['其他'] = tt[0]
                    else:
                        #                     print(tt)
                        res[tt[0]] = tt[1]

            return str(res)

    else:
        return ''


def handle_source(v, btm):
    '''
    input: 材料中的填报须知与来源
    out: 格式化后的信息  [ 法规明晨，文号，内容等 ]
    '''
    res = ''
    text1 = v
    if 'javascrip' in text1 and 'data-target' in text1:
        patj = 'data-target="(.*?)".*?填报须知'
        idsx = S_search(patj, text1)
        if idsx == "":
            return ""
        else:

            idsx = idsx.replace('#', '')
            text2 = btm.find_all(id=idsx)

            if len(text2) != 0:
                text2 = str(text2[0])
            else:
                text2 = ''
            #             print(text2)
            #             patbd = r'<table.*?>(.*?)</table>'
            patbd = '<div class="modal-bd">.*?<p>(.*?)</p>'
            text3 = S_search(patbd, text2)
            text3 = text3.replace('\n', '').replace('\t', '')
            res = '填报须知' + '(' + text3 + ')'
        #             print(res)

        patj = 'data-target="(.*?)".*?来源渠道'
        tmp = re.search(patj, text1)
        if tmp == None:
            idsx = ''
        else:
            idsx = tmp.groups()[0]
        #         idsx = S_search(patj,text1)
        if idsx == "":
            return ""
        else:

            idsx = idsx.replace('#', '')
            text2 = btm.find_all(id=idsx)

            if len(text2) != 0:
                text2 = str(text2[0])
            else:
                text2 = ''
            #             print(text2)
            #             patbd = r'<table.*?>(.*?)</table>'
            patbd = '<div class="modal-bd">(.*?)</div>'
            text3 = S_search(patbd, text2)
            text3 = text3.replace('\n', '').replace('\t', '')
            s2 = re.findall('<p>(.*?)</p>', text3, re.S)
            tdict = {}
            for s1 in s2:
                s1 = s1.split('：')
                tdict[s1[0]] = s1[1]

            if res == "":
                cflag = ''
            else:
                cflag = ','

            res = res + cflag + '来源渠道' + '(' + str(tdict) + ')'
            return res

    else:
        return ''


###############
# 获取设定依据的类
###############
class SettingBasis(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.basis_name = ''  ### 依据名称
        self.basis_description = ''  ### 依据描述
        pat = '<table class="bszn-table layui-table">.*?依据名称.*?</table>'
        s = re.search(pat, text, re.S)
        if s == None:
            self.text = None
        else:
            self.text = s.group()

    def get_basis_name(self):
        if self.text == None:
            return 0
        else:
            pat = '<tr>.*?依据名称.*?</tr>'
            result = re.search(pat, self.text, re.S)
            result = result.group()
            result = re.sub('href="#"', '', result)
            href = re.search('href="(.*?)"', result, re.S)
            if href == None:
                href = ''
            else:
                href = href.group(1)
            result = re.sub('<a.*?>.*?</a>', '', result)
            result = re.search('<div>(.*?)</div>', result, re.S)
            result = result.group(1)
            self.basis_name = result.strip() + href.replace('amp;', '')

    def get_basis_description(self):
        if self.text == None:
            return 0
        else:
            pat = '<td colspan="8">(.*?)</td>'
            infos = self.text.split('</tr>')
            infos = infos[1]
            description = re.search(pat, infos, re.S)
            description = description.group(1)
            self.basis_description = description.strip()

    def get_all_infos(self):
        self.get_basis_name()
        self.get_basis_description()
        if self.text == None:
            return 0
        else:
            tc1 = ['依据名称', '依据说明']
            tc2 = [self.basis_name, self.basis_description]

            self.fill_content(tc1, tc2)


###############
# 获取申请条件的类
###############
class ApplicationCondition(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.basis_and_condition_description = []  ### 依据和条件说明
        pat = '<td class="td-title">依据及条件描述</td>.*?<td colspan="8">.*?</td>'
        s = re.search(pat, text, re.S)
        if s == None:
            self.text = None
        else:
            self.text = s.group()

    def get_bacd(self):
        if self.text == None:
            return 0
        else:
            pat = '<td colspan="8">(.*?)</td>'
            result = re.search(pat, self.text, re.S)
            result = result.group(1).strip()
            self.basis_and_condition_description = result

    def get_all_infos(self):

        self.get_bacd()

        tc1 = ['依据条件及描述']
        tc2 = [self.basis_and_condition_description]

        self.fill_content(tc1, tc2)


###############
# 获取申请材料的类
###############
class ApplicationMaterial(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def get_all_infos(self):
        pass


###############
# 获取特殊环节的类
###############
class SpecialProcedure(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.tc1 = []
        self.tc2 = []
        pat = '<table class="bszn-table layui-table">.*?特殊环节名称.*?</table>'
        result = re.search(pat, text, re.S)
        if result == None:
            self.text = None
        else:
            result = result.group()
            result = result.split('<!--特殊环节-->')
            result = result[-1]
            self.text = result

    def get_info(self):
        if self.text == None:
            return 0
        else:
            infos = re.findall('<td.*?>(.*?)</td>', self.text, re.S)
            infos = [item.strip() for item in infos]
            self.tc1 = []
            self.tc2 = []
            for i in range(int(len(infos) / 2)):
                self.tc1.append(infos[2 * i])
                self.tc2.append(infos[2 * i + 1])

    def get_all_infos(self):
        self.get_info()

        self.fill_content(self.tc1, self.tc2)


###############
# 如果没有设定依据，则获取服务理由的类
###############
class ServiceBasis(BasicPage):
    def __init__(self, text):
        super().__init__()
        self.service = []
        pat = '<table class="bszn-table layui-table">.*?服务理由.*?</table>'
        s = re.search(pat, text, re.S)
        if s == None:
            self.text = None
        else:
            s = s.group()
            self.text = s

    def get_service_basis(self):
        if self.text == None:
            return 0
        else:
            r = self.text.split('</tr>')
            r = r[0]
            r = re.sub(re.compile('<a.*?>.*?</a>', re.S), '', r)
            r = re.findall('<td colspan="8">(.*?)</td>', r, re.S)
            self.service.append(r[0].strip())

    def get_appendix(self):
        if self.text == None:
            return 0
        else:
            r = self.text.split('</tr>')
            r = r[1]
            download_link_pat = 'download.*?href="(.*?)"'
            url_name_pat = 'url="(.*?)"'
            result_0 = re.findall(url_name_pat, r, re.S)
            result_1 = re.findall(download_link_pat, r, re.S)
            if len(result_1) == 0:
                self.service.append('无')
            else:
                result = result_0[0] + result_1[0]
                self.service.append(result)

    def get_all_infos(self):
        self.get_service_basis()
        self.get_appendix()
        if self.text == None:
            return 0
        else:
            tc1 = ['服务理由(服务依据)', '附件']
            self.fill_content(tc1, self.service)


class Guide(BasicPage):

    def __init__(self, browser, text, url, idx, pid):
        super().__init__()
        self.content['url'] = url
        self.content['last_level_id'] = idx
        self.content['pid'] = str(idx) + '_' + str(pid)
        self.infos = BasicInfo(text)  ### 基本信息
        self.setting_basis = SettingBasis(text)  ### 设定依据
        self.application_condition = ApplicationCondition(text)  ### 申请条件
        self.application_material = ApplicationMaterial(text)  ### 申请材料
        self.special_procedure = SpecialProcedure(text)  ### 特殊程序
        self.service_basis = ServiceBasis(text)  ### 服务依据

    def get_infos(self):
        ''' 利用上面的类生成基本信息'''
        r = self.infos.handle_infos()
        if r == 0:
            print(self.content['pid'] + '存在error，请手动处理')

    def get_setting_basis(self):
        self.setting_basis.get_all_infos()

    def get_application_condition(self):
        self.application_condition.get_all_infos()

    def get_application_material(self):
        self.application_material.get_all_infos()

    def get_special_procedure(self):
        self.special_procedure.get_all_infos()

    def get_service_basis(self):
        self.service_basis.get_all_infos()

    def handle_guide(self):
        try:
            self.get_infos()
            self.get_setting_basis()
            self.get_application_condition()
            self.get_application_material()
            self.get_special_procedure()
            self.get_service_basis()

            tc1 = ['基本信息',
                   '设定依据', '申请条件',
                   '申请材料', '特殊程序',
                   '服务依据']
            tc2 = [self.infos.content,
                   self.setting_basis.content, self.application_condition.content,
                   self.application_material.content, self.special_procedure.content,
                   self.service_basis.content]
            self.fill_content(tc1, tc2)
        except Exception as e:
            traceback.print_exc()
            exit(-1)


if __name__ == '__main__':
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=20140826105015016582&orgcode=-4188128443937240449&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=52000020160807212710000489&orgcode=-4188128443937240449&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn//eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=300BB1D357C744C88056165E88671A33&orgcode=-4188128443937240449&areacode520000&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=20140627154824010789&orgcode=-1510171065368362017&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=11520000009390236U2000805012000-01&orgcode=-1510171065368362017&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=11520000009390236U152200500500002&orgcode=-1510171065368362017&areacode=520000'
    # level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=52000020160811122221004285&orgcode=-8028705483080645826&areacode=520000'
    level3_url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_ty.bgt_bszn&istest=1&otheritemcode=300BB1D357C744C88056165E88671A33&orgcode=-4188128443937240449&areacode=520000'
    level3_html = requests.get(level3_url)
    level3_html.encoding = 'utf-8'
    level3_text = level3_html.text
    # level3_text = '<div>nihao</div>'
    # level3_text = '<div>nihao</div>'
    # level3_text.encode('GBK')
    # setting_basis = SettingBasis(level3_text)
    # setting_basis.get_all_infos()
    # print(setting_basis.content)
    #
    # application_condition = ApplicationCondition(level3_text)
    # application_condition.get_all_infos()
    # print(application_condition.content)
    #
    # special_procedure = SpecialProcedure(level3_text)
    # special_procedure.get_all_infos()
    # print(special_procedure.content)
    #
    basic_info = BasicInfo(level3_text)
    basic_info.handle_infos()
    print(basic_info.content)

    # service_basis = ServiceBasis(level3_text)
    # service_basis.get_all_infos()
    # print(service_basis.content)
