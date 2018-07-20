#
# coding=utf-8

'''
命令: python 该脚本名.py 需要发送的附件名 收件人的邮箱地址
需要在SendEmail类中定义几个参数

    sender: 发送人的邮箱

    mail_host: stmp服务器名称
    mail_user: stmp服务器用户名
    mail_password: stmp服务器口令

    title: 邮件标题
    content: 邮件内容

    path: 被发送附件的路径
'''

import sys
# import subprocess  # 如果执行shell可用
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail(object):

    def __init__(self, mail_name):

        self.port = 25
        self.sender = 'xxxxxxxxxx@xxx.com'
        self.receivers = mail_name
        # self.sender_name = 'xxxxxxxx'
        # self.receiver_names = 'xxxxxxxx'
        self.title = 'department classify work'
        self.content = 'we to classify today'

        # 第三方 SMTP 服务
        self.mail_host="smtp.xxx.com"  #设置服务器
        self.mail_user="xxxxxxx@xxx.com"    #用户名
        self.mail_password="xxxxxxxxx"   #口令

        # 附件发送的flag
        self.attachment = True

        # 附件发送的path
        self.path = ''

    # send function
    def sendFunc(self, filename):

        message = MIMEMultipart()

        # 邮件头
        message['From'] = self.sender
        message['To'] = self.receivers
        message['Subject'] = self.title

        # 正文
        message.attach(MIMEText(self.content, 'plain', 'utf-8'))

        # 附件
        if self.attachment:  # 是否发送附件
            complete_path = self.path + filename
            try:
                with open(complete_path, 'rb') as f:
                    file = f.read()
            except:
                # 'Mybe have not this file'
                raise IOError
            att = MIMEText(file, 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            # filename is filename in email attachment
            att["Content-Disposition"] = 'attachment; filename=%s' % filename
            message.attach(att)

        try:
            smtpObj = smtplib.SMTP(host=self.mail_host, port=self.port)  # 25 SMTP port
            smtpObj.login(self.mail_user, self.mail_password)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print "send email success"
        except smtplib.SMTPException, e:
            print e
            print "Error: send Failure"


if __name__ == '__main__':
    filename = sys.argv[1]
    mail_name = sys.argv[2]
    SendEmail(mail_name).sendFunc(filename)

