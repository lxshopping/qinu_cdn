#!/usr/bin/env python
# --*-- coding:utf-8 --*--
import codecs
import os
import sys
import json
from pymongo import *
import pickle
import time
import smtplib
from email.mime.text import MIMEText

mail_host = "smtp.exmail.qq.com"         #定义smtp服务器
# mail_to = "lixiang@anfan.com,dpf@anfan.com,li_xiang111@qq.com"  #邮件收件人
mail_to_mult = "lixiang@anfan.com,dpf@anfan.com,smh@anfan.com"  #邮件收件人
mail_from = "lixiang@anfan.com"       #邮件发件人
mail_pass = "Anfen123redhat"            #邮件发件人邮箱密码



while True:

    reload(sys)
    sys.setdefaultencoding('utf8') #gb2312,gbk
    print sys.getdefaultencoding() # 输出当前编码


    def Mail(mass_flow):
        # mass_flow.encode('gbk').decode('gbk').encode('utf-8')
        # print mass_flow
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        msg = MIMEText("%s\n\n超过500G流量的包,具体信息如下:\n %s" % (date, mass_flow))
        msg['Subject'] = "Qiniu CDN trigger"     #定义邮件主题
        msg['From'] = mail_from
        # msg['To'] = mail_to
        mail_to_list = mail_to_mult.split(',')
        print mail_to_list
        for mail_to in mail_to_list:
            msg['To'] = mail_to
            print mail_to

            try:
                s = smtplib.SMTP()                 #创建一个SMTP()对象
                s.connect(mail_host, "25")             #通过connect方法连接smtp主机，非加密方式
                s.starttls()                    #启动安全传输模式
                s.login(mail_from,mail_pass)          #邮箱账户登录认证
                s.sendmail(mail_from, mail_to, msg.as_string())   #邮件发送
                s.quit()       #断开smtp连接
            except Exception, e:
                print str(e)

        #链接MongoDB
    # def ConMongo(host,port,cur_db,username,password):
    #     client = MongoClient("host",port)
    #     db = client["cur_db"]
    #     db.authenticate("username","password")
    #     table = db.qiniu_item_data
    #     return table

    def ConMongo(host,port,cur_db):
        client = MongoClient("host",port)
        db = client.cur_db
        table = db.qiniu_item_data
        return table


    # def Log(message):
    #     f = file(lock_file,'ab')  # 注意换行
    #     f.write('\n'+message)
    #     f.close()

    # def load_file_list():
    #     with open('CreditCard.pk','r+') as fp:
    #         user_info = []
    #         while True:
    #             try:
    #                 file_dict = pickle.load(fp)
    #             except EOFError:
    #                 break
    #             else:
    #                 user_info.append(file_dict)
    #         return user_info


    # Conn = ConMongo('192.168.1.246',27017,'anfeng_spider')

    client = MongoClient("192.168.1.246",27017)
    db = client["anfeng_spider"]
    Conn = db.qiniu_item_data
    Conn.count()


    # 查询mongo item表中总条目

    total_data = Conn.count()

    print total_data

    # 查询mongo item表中流量大于500G的连接

    # [[],[],[]]
    # gt_list = []
    gt_list_total = []


    # 排除重定向的url，没有包的大小
    for item in Conn.find({"flow_value":{"$gt":236870912000}}):
        try:
            flow_message = '%d,%d,%s,%d,%d,%d,%d' % (item["start_time"],item["scrapy_time"],item["url"],item["flow_value"],item["apk_size"],item["download_count"],item["view_count"])
            print flow_message
            gt_list = flow_message.split(',')
            # gt_list.append(flow_message)
            print gt_list
            gt_list_total.append(gt_list)
            gt_list = []
            # print item["scrapy_time"],item["url"],item["flow_value"],item["apk_size"],item["download_count"],item["view_count"]
        except Exception as e:
            print e

    print gt_list_total
    print len(gt_list_total)

    with open('D:\qinu.new', 'ab+') as write_file:
        gt_number = len(gt_list_total)
        # write_file.write('%s'  % gt_number)
        # write_file.write(str(gt_number)+'\n')
        write_file.write("\n总个数: %s个\n\n"  % gt_number)



    for number in gt_list_total:
        print number
        with open('D:\qinu.new', 'ab+') as write_file:
            try:
                # line = 'time : %s\n url : %s\n traffic : %s\n apk_size : %s\n downloadcount : %s\n view_count : %s\n' % (number[0],number[1],number[2],number[3],number[4],number[5])
                line = '生成时间 : %s\n 采集时间 : %s\n url : %s\n 实际流量 : %sG\n 包大小 : %sM\n 下载次数 : %s\n 访问次数 : %s\n\n' % (time.strftime('%Y-%m-%d',time.localtime(int(number[0]))),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(number[1]))),number[2],int(number[3])/1024/1024/1024,int(number[4])/1024/1024,number[5],number[6])
                print line
            except Exception as e:
                print e
            write_file.write(line)

    with open('D:\qinu.new', 'ab+') as write_file:
        # readlines 读取所有
        message = write_file.read()
        # print message
        message.encode('utf-8')
        # print type(message)
        Mail(message)
        # write_file.truncate()

    with open('D:\qinu.new', 'w+') as write_file:
        clear_file = ''
        write_file.write(clear_file)

    # Mail(s)
    # Mail(item)
    # print "Ping %s successful." % item

    print "Sleep 60s..."
    time.sleep(60)


