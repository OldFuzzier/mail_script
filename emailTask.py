# /usr/bin/pyyhon
# coding=utf-8

import sys
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail(object):

    def __init__(self, mail_name):

        self.port = 25
        self.sender = 'xxxxxxxx@xxx.com'
        self.receivers = mail_name
        # self.sender_name = 'xxxxxxxx'
        # self.receiver_names = 'xxxxxxxx'
        self.title = 'department classify work'
        self.content = 'we to classify today'

        # 第三方 SMTP 服务
        self.mail_host="smtp.xxx.com"  #设置服务器
        self.mail_user="xxxxxxxx@xxx.com"    #用户名
        self.mail_pass="xxxxxxxxxxxxxx"   #口令

        self.attachment = True

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
            text_list = ['.crt', '.key']
            for text in text_list:
                path = '/etc/openvpn/easy-rsa/2.0/keys/%s' % filename + text
                print path
                try:
                    with open(path, 'rb') as f:
                        file = f.read()
                except IOError, e:
                    print e
                    print 'Mybe have not this file'
                    break
                att = MIMEText(file, 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                # filename is filename in email attachment
                att["Content-Disposition"] = 'attachment; filename=%s' % filename + text
                message.attach(att)

        try:
            smtpObj = smtplib.SMTP(host=self.mail_host, port=self.port)  # 25 SMTP port
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print "send email success"
        except smtplib.SMTPException, e:
            print e
            print "Error: send Failure"


class ScriptMail(SendEmail):

    def __init__(self, mail_name):
        super(ScriptMail, self).__init__(mail_name)

    # run shell
    def exec_shell(self, filename):
        cmd = 'ls /etc/openvpn/easy-rsa/2.0/keys/'
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        tempList = pipe.readlines()
        temp = [ele.strip() for ele in tempList]
        if filename not in temp:
            cmd = "/etc/openvpn/openvpn.sh %s" % filename
            subprocess.call(cmd)  # execute shell
        else:
            print 'The file have already exis'
            return

    # .key
    # .crt
    # /etc/openvpn/easy-rsa/keys

    def main(self, filename):
        self.exec_shell(filename)
        self.sendFunc(filename)


if __name__ == '__main__':
    filename = sys.argv[1]
    mail_name = sys.argv[2]
    sm = ScriptMail(mail_name)
    sm.main(filename)
