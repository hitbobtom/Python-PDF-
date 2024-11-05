# 发送邮件
# -*- codeing = utf-8 -*-

import smtplib
from email.mime.text import MIMEText


def getServer(sendAddress):
    # 发件人授权码
    password = 'POZGWBMHONHUVZPM'
    # 连接服务器
    server = smtplib.SMTP_SSL('smtp.163.com', 465)
    # 登录邮箱
    loginResult = server.login(sendAddress, password)
    print(loginResult)

    return server


def getMsg(subject,content):
    # 正文

    # 定义一个可以添加正文的邮件消息对象
    msg = MIMEText(content, 'plain', 'utf-8')

    # 发件人昵称和地址
    msg['From'] = 'qitongfu<xxx@qq.com>'
    # 收件人昵称和地址
    msg['To'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
    # 抄送人昵称和地址
    msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
    # 邮件主题
    msg['Subject'] = subject

    return msg


def sendMail(subject, content):
    # 发件人邮箱地址
    sendAddress = 'sunnywaphy@163.com'
    # 收件人邮箱地址
    toAddress = 'sunnywaphy@163.com'
    server = getServer(sendAddress)
    msg = getMsg(subject,content)
    server.sendmail(sendAddress, toAddress, msg.as_string())
    print('发送成功')


if __name__ == "__main__":
    sendMail("下载成功","下载成功")
