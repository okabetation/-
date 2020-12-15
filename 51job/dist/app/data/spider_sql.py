#-*- codeing = utf-8 -*-
#@Time : 2020/11/9 11:51
#@Author : OT
#@File : spider_mysql.py
#@Software : PyCharm

#sqlite存储
import requests
import re
import json
import sqlite3

# 数据库储存
def savaDataDb(datalist,datapath):
    init_db(datapath)
    conn = sqlite3.connect(datapath)
    cur = conn.cursor()
    i=0
    for data in datalist:
        i=i+1
        for index in range(len(data)):
            data[index]= '"'+data[index]+'"'
        sql = '''
                insert into job (
                job_name, company_href, company_name, companytype_text, jobwelf, attribute_text, companyind_text,providesalary_text,company_address,company_school)
                values(%s)'''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
        print('第%d条数据爬取成功'%i)
    cur.close()
    conn.close()

#数据库创建
def init_db(datapath):
    sql = '''
        create table job
        (

        id integer primary key autoincrement,
        job_name text,
        company_href text,
        company_name text,
        companytype_text text,
        jobwelf text ,
        attribute_text text ,
        companyind_text text ,
        providesalary_text text ,
        company_school text,
        company_address text 
        )

    '''

    conn = sqlite3.connect(datapath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

#数据爬取
def askurl(page):
    datalist= []
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%s,2,%d.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    work = input('请输入需要查询的职业')
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    params = {
        'lang':'c',
        'postchannel':'0000',
        'workyear':'99',
        'cotype':'99',
        'degreefrom':'99',
        'jobterm':'99',
        'companysize':'99',
        'ord_field':'0',
        'dibiaoid':'0',
        'line':'',
        'welfare':'',
    }
    ex = r'window.__SEARCH_RESULT__ = (.*)</script>'
    for k in range(1,page):
        url_data = url%(work,k)
        response = requests.get(url=url_data,headers=headers,params=params).text
        re_data = re.findall(ex,response)[0]
        json_data = json.loads(re_data)
        work_data = json_data["engine_search_result"]
        for li in range(0,len(work_data)):
            job_name = work_data[li]['job_name']    #职位名称
            company_href = work_data[li]['company_href']    #详情连接
            company_name = work_data[li]['company_name']    #公司名称
            companytype_text = work_data[li]['companytype_text']    #公司人数
            jobwelf = work_data[li]['jobwelf']      #公司福利
            try:
                if  len(work_data[li]['attribute_text']) == 3:
                    company_adress = work_data[li]['attribute_text'][0]  # 公司地点
                    company_school = work_data[li]['attribute_text'][1]  # 学历要求
                else:
                    company_adress = work_data[li]['attribute_text'][0]  # 公司地点
                    company_school = work_data[li]['attribute_text'][2]  # 学历要求
            except Exception:
                continue
            attribute_text = ' '.join(work_data[li]['attribute_text'])    #整体需求
            # 数组 ['上海', '1年经验', '本科', '招若干人']
            companyind_text = work_data[li]['companyind_text']  #公司类型
            # if work_data[li]['providesalary_text'] == '':   #薪资
            #     providesalary_text ='面议'
            # else :
            #     providesalary_text = work_data[li]['providesalary_text']
            providesalary_text = work_data[li]['providesalary_text']
            all_list = [job_name,company_href,company_name,companytype_text,jobwelf,attribute_text,companyind_text,providesalary_text,company_adress,company_school]
            datalist.append(all_list)
            print(all_list)
    # print(datalist)
            if k == 1:
                print('成功爬取第%d条'%(li+1))
            else:
                print('成功爬取第%d条' % ((li + 1)+(50*k)))
    return datalist



if __name__ == "__main__":
   datalist = askurl(50)
   datapath = "51job.db"
   # print(datalist)
   # savaDataDb(datalist,datapath)





