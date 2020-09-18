#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json


# In[9]:


def handle_indent(lines):
    '''
    处理包含有indent的数据
    input: lines
    outpur :  list[dict,dict]
    '''
    res_lst = []
    res = ''
    for line in lines:
        line = line.replace('\n','')
        if line == '{':
            line = line.strip()
            res = '{'
        elif line == '}':
            line = line.strip()
#             print('*****')
            res += line
            rt =eval(res)
            res_lst.append(rt)
#             print(rt)
        else:
            line = line.strip()
            res += line
    return res_lst


# In[2]:


with open('0.json','r',encoding='utf-8') as f:
#     aa = json.load(f)
    lines = f.readlines()
f.close()


# In[11]:


res_lst = handle_indent(lines)


# In[15]:


with open('0000.json','w+',encoding = 'utf-8') as f:
    json.dump(res_lst,f,ensure_ascii = False,indent = 4)
f.close()


# ### 加载数据

# In[16]:


with open('0000.json','r',encoding = 'utf-8') as f:
    clst = json.load(f)
f.close()


# In[ ]:




